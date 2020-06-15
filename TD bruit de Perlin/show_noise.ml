#load "graphics.cma";;
let show_noise noise = 
	let size = [|500; 500|] in
	let pas = 3 in
	Graphics.open_graph ((string_of_int size.(0))^"x"^(string_of_int size.(1)));
	for x = 0 to size.(0)/pas do
		for y = 0 to size.(1)/pas do
			let c = int_of_float (((noise (float_of_int (x*pas)) (float_of_int (y*pas)))+.1.)*.128.) in
			Graphics.set_color (Graphics.rgb c c c);
			Graphics.fill_rect x y pas pas done done;;
