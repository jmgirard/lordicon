module.exports = {
	"entry": "./src/main.js",
	"mode": "production",
	"output": {
		"path": `${__dirname}/_extensions/lordicon/assets/js/`,
		"filename": "bundle.js",
	},
  "module": { 
    "rules": [ 
		{ 
		  "test": /\.css$/, 
		  "use": [ "style-loader", "css-loader" ],
		}, 
		{ 
		  "test": /\.js$/, 
		  "exclude": /node_modules/, 
		  "use": { 
			"loader": "babel-loader", 
			"options": { 
			  "presets": [
					["@babel/preset-env", { 
						"debug": true,
					}],
				],
			},
		  }, 
		}, 
	], 
  },
};
