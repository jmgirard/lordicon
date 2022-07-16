module.exports = {
	entry: './_extensions/lordicon/assets/js/main.js',
	mode: 'production',
	output: {
		path: `${__dirname}/_extensions/lordicon/assets/js/`,
		filename: 'bundle.js',
	},
	module: {
		rules: [
			{
				test: /\.css$/,
				use: [
					'style-loader',
					'css-loader',
				],
			},
		],
	},
};
