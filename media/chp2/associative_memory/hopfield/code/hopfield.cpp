#include <sstream>
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

#include <opencv2/opencv.hpp>

// Some constants
const float KEEP_RATIO = 0.3f;
const int ITERATION_COUNT = 10;

/*
 * Visualisation
 */
const int BORDER = 2;

void imshow(cv::Mat_<float> &tar, const cv::Mat_<float> &src, int i, int j) {
	int w = src.cols;
	int h = src.rows;
	src.copyTo(tar(cv::Rect(i * (w + 2 * BORDER) + BORDER, j * (h + 2 * BORDER) + BORDER, w, h)));
}

void imwrite8b(const char *fn, const cv::Mat_<float> &in) {
	cv::Mat_<uint8_t> img(in.rows, in.cols);
	for (int i = 0; i < in.rows * in.cols; i++) {
		img(i) = in(i) > 0.0f ? 255 : 0;
	}
	imwrite(fn, img);
}

void prepare_tiles(cv::Mat_<float> &tar, int w, int h, int tx, int ty) {
	const int tw = (w + 2 * BORDER) * tx;
	const int th = (h + 2 * BORDER) * ty;
	if (tar.cols != tw && tar.rows != th) {
		tar = cv::Mat_<float>::ones(th, tw);
	}
}

/**
 * Function for reading the images and converting to a range between -1.0f and 1.0f
 */
cv::Mat_<float> readPatternVector(int &w, int &h, const std::string &fn)
{
	cv::Mat_<uint8_t> img = cv::imread(fn, CV_LOAD_IMAGE_GRAYSCALE);

	// Check the output matrix as a proper size
	const int iw = img.cols;
	const int ih = img.rows;
	if (img.empty() || (w > 0 && iw != w) || (h > 0 && ih != h)) {
		throw "Error while loading image " + fn;
	}
	w = iw;
	h = ih;

	// Convert the input matrix to a floating point matrix
	cv::Mat_<float> res(w, h);
	img.convertTo(res, CV_32F, 1.0f / 128.0f, -1.0f);
	return res.reshape(1, w * h);
}

/**
 * Function for adding noise to the image
 */
void addNoise(cv::Mat_<float> &img)
{
	cv::RNG rng;
	for (int x = 0; x < img.cols; x++) {
		for (int y = 0; y < img.rows; y++) {
			img(y, x) = img(y, x) * rng.uniform(0.0f, 1.0f) > (1.0f - KEEP_RATIO) ? 1.0f : -1.0f;
		}
	}
}

/**
 * Training using the heb rule.
 */
void trainNetworkHebb(cv::Mat_<float> &weights,
		const cv::Mat_<float> &p, const float f)
{
	// Fetch the number of neurons
	const int n = p.rows;

	// Make sure the weight matrix is not empty
	if (weights.empty()) {
		weights = cv::Mat_<float>::zeros(n, n);
	}

	// Heeb training
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (i == j) {
				continue;
			}
			weights(i, j) = weights(i, j) + f * p(i) * p(j);
		}
	}
}

float iterateHopfieldNeuron(const int i, cv::Mat_<float> &activations,
		const cv::Mat_<float> &weights)
{
	// Fetch the number of neurons
	const int n = weights.rows;

	float s = 0.0f;
	for (int j = 0; j < n; j++) {
		s += weights(i, j) * activations(j);
	}
	if (s > 0) {
		return 1.0f;
	} else {
		return -1.0f;
	}
}


/**
 * Synchronous simulation of the network
 */
void iterateNetwork(cv::Mat_<float> &activations, const cv::Mat_<float> &weights)
{
	// Fetch the number of neurons
	const int n = weights.rows;

	// Make sure the activation matrix is not empty
	if (activations.empty()) {
		activations = cv::Mat_<float>::zeros(n, 1);
	}
	cv::Mat_<float> aIn = activations.clone();
	cv::Mat_<float> &aOut = activations;

	// Apply the hopfield neuron rule
	for (int i = 0; i < n; i++) {
		aOut(i) = iterateHopfieldNeuron(i, aIn, weights);
	}
}

/**
 * Asynchronously iterates the network.
 */
void iterateNetworkAsync(cv::Mat_<float> &activations,
		const cv::Mat_<float> &weights, std::vector<int> &indices,
		int numIterations)
{
	// Fetch the number of neurons
	const int n = weights.rows;

	// Make sure the activation matrix is not empty
	if (activations.empty()) {
		activations = cv::Mat_<float>::zeros(n, 1);
	}

	// Apply the hopfield neuron rule to a single neuron at a time
	cv::RNG rng;
	if (indices.empty()) {
		for (int i = 0; i < n; i++) {
			indices.push_back(i);
		}
	}
	for (int iter = 0; iter < numIterations; iter++) {
		int idx = rng.uniform(0, indices.size());
		int i = indices[idx];
		activations(i) = iterateHopfieldNeuron(i, activations, weights);
		indices.erase(indices.begin() + idx);
	}
}

int main(int argc, char *argv[])
{
	char str[255];
	int w{-1}, h{-1};
	cv::Mat_<float> weights;
	cv::Mat_<float> resultVisualisation;
	try {
		// Train the network on the given input images
		std::vector<std::string> patterns;
		for (int i = 1; i < argc; i++) {
			patterns.push_back(argv[i]);
		}
		std::vector<cv::Mat_<float>> imgs;
		{
			int idx = 0;
			const float f = 1.0f / (float)patterns.size();
			for (std::string &fn: patterns) {
				// Read the image
				std::cout << "Reading pattern " << fn << std::endl;
				cv::Mat_<float> img = readPatternVector(w, h, fn);

				sprintf(str, "out/%02d_00_orig.png", idx);
				imwrite8b(str, img.reshape(1, h));

				// Make sure the output image has the correct size
				prepare_tiles(resultVisualisation, w, h, ITERATION_COUNT + 2, patterns.size());

				// Train the network
				std::cout << "Training pattern " << fn << std::endl;
				trainNetworkHebb(weights, img, f);

				// Show the image
				imshow(resultVisualisation, img.reshape(1, h), 0, idx);

				// Add some noise to the image and store the noisy image
				addNoise(img);
				imshow(resultVisualisation, img.reshape(1, h), 1, idx);
				imgs.push_back(img);

				sprintf(str, "out/%02d_01_noise.png", idx);
				imwrite8b(str, img.reshape(1, h));

				idx++;
			}
		}

		// Iterate over all input stimuli
		{
			int idx = 0;
			for (cv::Mat_<float> &input : imgs) {
				std::cout << "Testing pattern " << patterns[idx] << std::endl;
				cv::Mat_<float> activations = input.clone();
				std::vector<int> indices;
				for (int i = 0; i < ITERATION_COUNT; i++) {
					//iterateNetwork(activations, weights);
					iterateNetworkAsync(activations, weights, indices, w * h / 4);
					imshow(resultVisualisation, activations.reshape(1, h), 2 + i, idx);

					sprintf(str, "out/%02d_%02d_activation.png", idx, 2 + i);
					imwrite8b(str, activations.reshape(1, h));
				}
				idx++;
			}
		}

		cv::Mat_<float> resultVisualisation2x;
		cv::resize(resultVisualisation, resultVisualisation2x, cv::Size(), 2.0, 2.0, cv::INTER_NEAREST);
		imshow("Result", resultVisualisation);
		imwrite8b("out/result.png", resultVisualisation);
		cv::waitKey(0);
	} catch (std::string s) {
		std::cout << "Error: " << s << std::endl;
		return 1;
	}
	return 0;
}

