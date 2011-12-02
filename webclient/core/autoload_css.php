<?php
/**
 * Dynamic load css file system
 *
 * @package Core
 * @version 0.1
 * @author
 * Francisco Jesús Hidalgo González
 *
 *
 */

class CSS_load {
    /**
     * Constructor
     */
    public function __construct() {}

    /**
	 * Load all css files.
	 */
    public function load_all_css_files() {
        $path = APP_ROOT.'/css';
        $dir = opendir($path);

        while (($file = readdir($dir)) !== false) {
            if (is_dir(APP_ROOT.'/css/'.$file) && $file != '.' && $file != '..') {
                $d = opendir(APP_ROOT.'/css/'.$file);
                while (($f = readdir($d)) !== false) {
                    if (!is_dir(APP_ROOT.'/css/'.$file.'/'.$f) && $f != '.' && $f != '..' && strstr($f, '.css')) {
                        echo '<link rel="stylesheet" href="http://'.SERVER_NAME.APP_DIR.'/css/'.$file.'/'.$f.'" type="text/css" />'."\n";
                    }
                }
                closedir($d);
            }
        }
        closedir($dir);
    }
}
?>