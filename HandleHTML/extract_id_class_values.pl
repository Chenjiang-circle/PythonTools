#!/usr/bin/perl

use File::Basename;
# $dir = "./非播放页面html/*.html";
# $out_dir = "./test1";

$dir = $ARGV[0];  # 参数一，待提取的html存放路径
$out_dir = $ARGV[1];  # 参数二，提取出来的结果的输出路径

$out_id_dir = $out_dir . "/id";  # 对输出路径进行进一步分类，分为id和class
$out_class_dir = $out_dir . "/class";
mkdir($out_dir);  # 创建输出路径
mkdir($out_id_dir);
mkdir($out_class_dir);
@files = glob($dir);  # 读取html文件

foreach $file (@files) {
    $file_name = fileparse($file, qr/\.[^.]*/);  # 获取html文件名（除去路径，后缀）
    open($html_file, "$file") or die "$file 文件无法打开，$!";  # 打开文件

    $output_id = $out_id_dir . "/" . $file_name . ".txt";  # 提取的id属性值的输出文件路径
    open($output_file_id, ">$output_id") or die "$output_id 文件无法打开，$!";

    $output_class = $out_class_dir . "/" . $file_name . ".txt";  # 提取的class属性的输出文件路径
    open($output_file_class, ">$output_class") or die "$output_class 文件无法打开，$!";
    
    while (<$html_file>) {
        while ($_ =~ m/\s+id="(.*?)?"/g) {  # 正则匹配id属性值
            print $output_file_id "$1\n";  # 将匹配结果输出
        }
        while ($_ =~ m/\s+class="(.*?)?"/g) {  # 正则匹配class属性值
            print $output_file_class "$1\n";  # 将匹配结果输出
        }
    }
    close($html_file);
    close($output_file_id);
    close($output_file_class);
}
