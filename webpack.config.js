const path = require('path');

module.exports = {
	entry: {
		main: './bbq_organizer/static_dev/js/index.js',
		create_event: './bbq_organizer/static_dev/js/create-event.js',
		register: './bbq_organizer/static_dev/js/register.js'
	},
	resolve: {
		modules: [path.resolve(__dirname, "app"), "node_modules"],
	},
	module: {
		rules: [
			{
				test: /\.s[ac]ss$/i,
				use: [
					'style-loader',
					'css-loader',
					'sass-loader',
				],
			},
		],
	},
	output: {
		filename: '[name].js',
		path: path.resolve(__dirname, 'bbq_organizer/static/js')
	},
};
