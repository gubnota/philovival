<?php
$d = __DIR__;
$k =["en.txt","es.txt","hi.txt","id.txt","ja.txt","pt.txt","ru.txt","tr.txt","vi.txt","zh.txt"];
$b = "en.txt";
$g = file("$d/$b");
foreach($k as $a){
$fa = file("$d/$a");
$out = '{"contents":[';
for($i=0; $i<count($g); $i++){
// echo "k: \"$($g[$i])\" v: \"{$fa[$i]}\", lang:$a\n";
//'{"k": "OK","v": "Согласен"},';
$out .= '{"k": "';
$out .= rtrim($g[$i]);
$out .= '", "v": "';
$out .= rtrim($fa[$i]);
$out .= '"},';
}
$out = substr($out,0, strlen($out)-1);
$out .= ']}';

$file_name = "$d/";
$file_name .= substr($a,0,2);
$file_name .= ".json";
// echo "$file_name\n\n";
// echo $out;
// echo "\n\n";
file_put_contents($file_name, $out);
}
?>