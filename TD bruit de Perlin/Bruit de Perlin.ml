"1)";;
let element_aleatoire liste = 
	let n = List.length !liste in
	let rec aux rank l = match rank with
		0 -> let h::t = l in liste:=t; h
		|_-> let h::t = l in let elt = aux (rank-1) t in liste:= h::(!liste); elt
	in aux (Random.int n) !liste;;

"2)";;
let liste_aleatoire n = 
	let nombres = ref [] in
	for i = 0 to n-1 do nombres:= i::!nombres done;
	let entiers = ref [] in
	for i = 0 to n-1 do entiers:= (element_aleatoire nombres)::!entiers done;
	Array.of_list !entiers;;

"3)";;
let vecteur_unitaire () = let diag = 2.**0.5/.2. in
	[|(1.,0.);(0.,1.);(-1.,0.);(0.,-1.);(diag,diag);
	(-.diag,diag);(diag,-.diag);(-.diag,-.diag)|];;

"4)";;
let modulo x n = if x >= 0 then x mod n else (x mod n)+n;;
(*en Caml, l'operateur peux renvoyer des nombres négatifs, attention*)

let obtenir_vecteur x y vecteurs entiers = 
	let n = Array.length entiers in let m = Array.length vecteurs in
	let k = entiers.(modulo (y+entiers.(modulo x n)) n) in
	vecteurs.(k mod m);;

"5)";;
let scalaire v1 v2 = 
	let x1, y1 = v1 in 
	let x2, y2 = v2 in 
	x1*.x2 +. y1*.y2;;

let vecteur x1 y1 x2 y2 = (x2 -. x1, y2 -. y1);;

"6-10)";;
let tf = float_of_int;;
let ti = int_of_float;;
(*on réécrit ses fonctions avec moins de caractères poour que le code soit plus lisible par la suite*)

let generer_bruit_de_perlin resolution = 
	let res = resolution in
	let entiers = liste_aleatoire 256 in
	let vecteurs = vecteur_unitaire () in
	
	let bruit_de_perlin x y = 
		let x = x/.res in
		let y = y/.res in
		let x0 = ti x in
		let y0 = ti y in
		let x1 = x0 + 1 in
		let y1 = y0 + 1 in
		
		let tdx = x -. (tf x0) in
		let tdy = y -. (tf y0) in
		let dx = 3.*.tdx*.tdx -. 2.*.tdx*.tdx*.tdx in
		let dy = 3.*.tdy*.tdy -. 2.*.tdy*.tdy*.tdy in
		
		let u1 = obtenir_vecteur x0 y0 vecteurs entiers in
		let v1 = vecteur (tf x0) (tf y0) x y in
		let s_x0y0 = scalaire u1 v1 in
		let u2 = obtenir_vecteur x1 y0 vecteurs entiers in
		let v2 = vecteur (tf x1) (tf y0) x y in
		let s_x1y0 = scalaire u2 v2 in
		let u3 = obtenir_vecteur x0 y1 vecteurs entiers in
		let v3 = vecteur (tf x0) (tf y1) x y in
		let s_x0y1 = scalaire u3 v3 in
		let u4 = obtenir_vecteur x1 y1 vecteurs entiers in
		let v4 = vecteur (tf x1) (tf y1) x y in
		let s_x1y1 = scalaire u4 v4 in
		
		let l1 = s_x1y0*.dx +. s_x0y0*.(1.-.dx) in
		let l2 = s_x1y1*.dx +. s_x0y1*.(1.-.dx) in
		let l = l2*.dy +. l1*.(1.-.dy) in
		l
	in bruit_de_perlin;;

"11)";;
let generer_bruit_de_perlin_2 resolution = 
	let pi = cos (-1.) in
	let p1 = generer_bruit_de_perlin resolution in
	let p2 = generer_bruit_de_perlin (resolution*.pi/.2.) in
	let perlin x y =
		(p1 x y +. p2 x y) /. 2.
	in perlin;;

"12)";;
let generer_bruit_de_perlin_3 layers = 
	let total = ref 0. in
	let perlins = ref [] in
	let rec aux layer = match layer with
		[] -> ()
		|(resolution, coeficiant)::t -> total := !total +. coeficiant; perlins := (generer_bruit_de_perlin resolution, coeficiant)::!perlins; aux t
	in aux layers;
	let perlin x y =
		let rec noise layer = match layer with
			[] -> 0.
			|(perl, coef)::t -> (coef*. perl x y) +. noise t
		in noise !perlins /. !total
	in perlin;;

"13)";;
let increment nombre base = 
	let n = Array.length !nombre in
	let i = ref 0 in
	!nombre.(0) <- 1+ !nombre.(0);
	while !i < n && !nombre.(!i) = base do
		!nombre.(!i) <- 0;
		incr i;
		if !i < n then !nombre.(!i) <- !nombre.(!i) +1 done;;

"14)";;
(*permet de conter le nombre de 0 dans une array*)
let nbZeros n indice = 
	let nb = ref 0 in
	for i = 0 to n-1 do
		if !indice.(i) = 0 then incr nb done; !nb;;
(*la bijection entre l'écriture en base 3 et les vecteurs unitaires*)
let get_vecteur_bijection indice unit = 
	let n = Array.length !indice in
	let zeros = nbZeros n indice in
	let coef = !unit.(n-1-zeros) in
	let vecteur = Array.make n 0. in
	for i = 0 to n-1 do
		if !indice.(i) = 1 then vecteur.(i) <- coef else (if !indice.(i) = 2 then vecteur.(i) <- -.coef) done;
	vecteur;;

let vecteurs_dimension_n n = 
	let unit = ref (Array.make n 0.) in
	for i = 1 to n do
		!unit.(i-1) <- (((float_of_int i)**0.5)/.(float_of_int i)) done;
	let vecteurs = ref [] in
	let indice = ref (Array.make n 0) in
	let nul = Array.make n 0 in
	increment indice 3;
	while !indice <> nul do
		vecteurs := (get_vecteur_bijection indice unit)::!vecteurs;
		increment indice 3 done; Array.of_list !vecteurs;;

"15)";;
let obtenir_vecteur p vecteurs entiers = 
	let n = Array.length entiers in
	let m = Array.length vecteurs in 
	let k = ref 0 in
	for i =0 to Array.length p -1 do
		k := modulo (p.(i) + entiers.(!k)) n done;
	vecteurs.(modulo !k m);;

let scalaire_n v1 v2 = 
	let n = Array.length v1 in
	let scal = ref 0. in
	for i = 0 to n-1 do
		scal := !scal +. v1.(i)*.v2.(i) done; !scal;;

let vecteur_n p1 p2 = 
	let n = Array.length p1 in
	let v = Array.make n 0. in
	for i = 0 to n-1 do
		v.(i) <- p2.(i) -. p1.(i) done; v;;

let generer_bruit_de_perlin_n resolution n = 
	let res = resolution in
	let vecteurs = vecteurs_dimension_n n in
	let entiers = liste_aleatoire ((Array.length vecteurs)*(Array.length vecteurs)) in
	
	let bruit_de_perlin point = 
		(*initialisation*)
		let p = Array.make n 0. in
		let p0 = Array.make n 0 in
		let p1 = Array.make n 0 in
		for i = 0 to n-1 do 
			p.(i) <- point.(i)/.res;
			p0.(i) <- ti p.(i);
			p1.(i) <- p0.(i) + 1 done;
		
		let dp = Array.make n 0. in 
		for i = 0 to n-1 do
			let dx = p.(i) -. tf p0.(i) in
			dp.(i) <- 3.*.dx*.dx -. 2.*.dx*.dx*.dx done;
		
		(*calcul des scalairs*)
		let indicateur = ref (Array.make n 0) in
		let nPower = (ti(2.**(tf n))) in
		let s = Array.make nPower 0. in
		for i = 0 to nPower-1 do
			let vi = Array.make n 0 in
			let vf = Array.make n 0. in
			(* calcul du vecteur v grace a la bijection entre l'écriture en base 2 et les vecteur p0 ou p1*)
			for j = 0 to n-1 do
				if !indicateur.(j) = 0 then vf.(j) <- tf p0.(j) else vf.(j) <- tf p1.(j);
				if !indicateur.(j) = 0 then vi.(j) <- p0.(j) else vi.(j) <- p1.(j) done;
			let u = vecteur_n vf p in
			s.(i) <- scalaire_n u (obtenir_vecteur vi vecteurs entiers);
			increment indicateur 2 done;
		
		(*calcul des interpolation*)
 		let l = ref [s] in
		for i = 0 to n-1 do
			let h::t = !l in
			let temp = Array.make ((Array.length h)/2) 0. in
			for j = 0 to (Array.length h)/2 -1 do
				(*Les coeficiant on été créés dans un ordre tel que
				les valeurs à interpoler soit toujours voisines l'une de l'autre dans l'array*)
				temp.(j) <- h.(2*j+1)*.dp.(i) +. h.(2*j)*.(1.-.dp.(i)) done;
			l := temp::!l done;
		let h::t = !l in
		h.(0)
	in bruit_de_perlin;;
