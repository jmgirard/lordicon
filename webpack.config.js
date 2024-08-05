const TerserPlugin = require('terser-webpack-plugin')
module.exports = {
	"entry": "./src/main.js",
	"output": {
		"path": `${__dirname}/_extensions/lordicon/assets/js/`,
		"filename": "bundle.js",
	},
  "module": { 
    "rules": [ 
		  { 
  		  "test": /\.js$/, 
  		  "exclude": /node_modules/, 
  		  "use": { 
  			  "loader": "babel-loader", 
  			  "options": { 
  			    "presets": ["@babel/preset-env"],
  			  },
  			},
  		}, 
    ], 
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
  mode: 'production'
};
