<?php
/**
 * Dynamic load js file system
 *
 * @package Core
 * @version 0.1
 * @author
 * Francisco Jesús Hidalgo González
 *
 * 
 */

class Javascript_load {

    var $js_needed = array(
                        'common/jquery.js',
                        'common/jquery-ui.js',
                        'common/jquery.bubblepopup.v2.3.1.min.js',
                        'common/growl.js',
                        'common/spin.min.js',
                        'strophejs-1.0.2/strophe.js',
                        'common/sha1.js',
                        'common/i18n.js',
                        'common/lang.es.js',
                        'common/xmpp.debug.js',
                        'common/xmpp.js',
                        'common/fileuploader.js',
                        'common/highcharts.js',
                        'common/common.js'
    );
    
    /**
     * Constructor
     */
    public function __construct() {
        foreach ($this->js_needed as $js) {
            echo '<script type="text/javascript" src="http://'.SERVER_NAME.APP_DIR.'/js/'.$js.'"></script>'."\n";
        }
    }

    /**
	 * Load all js files.
	 */
    public function load_all_js_files() {
        $path = APP_ROOT.'/js';
        $dir = opendir($path);

        while (($file = readdir($dir)) !== false) {
            if (is_dir(APP_ROOT.'/js/'.$file) && $file != '.' && $file != '..') {
                $d = opendir(APP_ROOT.'/js/'.$file);
                while (($f = readdir($d)) !== false) {
                    if (!is_dir(APP_ROOT.'/js/'.$file.'/'.$f) && $f != '.' && $f != '..' && strstr($f, '.js')) {
                        $js_file = $file.'/'.$f;
                        if (!in_array($js_file , $this->js_needed)) {
                            echo '<script type="text/javascript" src="http://'.SERVER_NAME.APP_DIR.'/js/'.$file.'/'.$f.'"></script>'."\n";
                        }
                    }
                }
                closedir($d);
            }
        }
        closedir($dir);
    }
}
?>