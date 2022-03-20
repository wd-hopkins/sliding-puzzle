import * as a1lib from '@alt1/base';

// Tell webpack to add index.html and appconfig.json to output
require("!file-loader?name=[name].[ext]!./index.html");
require("!file-loader?name=[name].[ext]!./appconfig.json");

const SPACING = 20;
const TILE_SIZE = 40;
const BORDER_WIDTH = 17;

const imgs = a1lib.ImageDetect.webpackImages({
	homeport: require("./homebutton.data.png"),
	elves: require("../assets/Elves\ puzzle\ solved.data.png")
});

document.addEventListener("DOMContentLoaded", run);

function tiles(full_board: ImageData): Array<Array<ImageData>> {
	var tiles = [...Array(5)].map(e => Array(5));
	for (let i = 0; i < 5; i++) {
		let x = BORDER_WIDTH + i * TILE_SIZE + i * SPACING;
		for (let j = 0; j < 5; j++) {
			let y = BORDER_WIDTH + j * TILE_SIZE + j * SPACING;
			var slice: ImageData = new ImageData(TILE_SIZE, TILE_SIZE);
			full_board.copyTo(slice, x, y, TILE_SIZE, TILE_SIZE, 0, 0);
			tiles[i][j] = slice;
		}
	}
	return tiles;
}

function run() {
	imgs.promise.then(() => {
		var tiles_arr = tiles(imgs.elves);
		document.getElementById("visual-result").innerHTML = '';
		for (let i = 0; i < 5; i++) {
			for (let j = 0; j < 5; j++) {
				document.getElementById("visual-result").append(tiles_arr[i][j].show());				
			}
		}
	});
}

a1lib.PasteInput.listen(ref => {
	// Calculate positions of tiles
	// 2*14 + 5*49 + 4*8
	var found_tiles = tiles(imgs.elves).map(row => row.map(tile => ref.findSubimage(tile)));
	console.log(found_tiles);
	
	// found_tiles.forEach(row => row.forEach(v => console.log(v)));
});

// You can reach exports on window.TEST because of
// config.makeUmd("testpackage", "TEST"); in webpack.config.ts
export function capture() {
	const img = a1lib.captureHoldFullRs();
	const loc = img.findSubimage(imgs.homeport);
	document.getElementById("result").innerText = "Found result: " + JSON.stringify(loc);

	if (loc.length != 0) {
		alt1.overLayRect(a1lib.mixColor(255, 255, 255), loc[0].x, loc[0].y, imgs.homeport.width, imgs.homeport.height, 2000, 3);
	} else {
		alt1.overLayTextEx("Couldn't find homeport button", a1lib.mixColor(255, 255, 255), 20, Math.round(alt1.rsWidth / 2), 200, 2000, "", true, true);
	}
	// Get raw pixels of image and show on screen (used mostly for debug)
	const buf = img.toData(loc[0].x - 100, loc[0].y - 100, 200, 200);
	document.getElementById("visual-result").innerHTML = '';
	document.getElementById("visual-result").append(buf.show());
}

// a1lib.on('alt1pressed', () => capture());

if (window.alt1) {
	// Tell alt1 about the app (this makes alt1 show the add app button when running inside the embedded browser)
	// Also updates app settings if they are changed
	alt1.identifyAppUrl("./appconfig.json");
}
