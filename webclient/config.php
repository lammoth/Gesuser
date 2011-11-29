<?
/**
 * @ignore
 * @package default
 */

// DEBUG:
	define('DEBUG', false);

	
//Login options
	define('SESSION_NAME', 'g3suser');
	
//Installation path options
	$paths = get_Paths();
	define('SERVER_NAME', $paths['SERVER_NAME']);
	define('APP_DIR', $paths['APP_DIR']);
	define('APP_ROOT', $paths['APP_ROOT']);
	define('UPLOAD_PATH',$paths['UPLOAD_PATH']);

	
	if(DEBUG)
		print_r($paths);
	
//Autoload class system
	include_once(APP_ROOT."/core/autoload.php");
//Autoload js system
    include APP_ROOT."/core/autoload_js.php";
//Autoload css system
    include APP_ROOT."/core/autoload_css.php";
	
/*********************************************************************************************************
 * Helper functions.
 *********************************************************************************************************/	
	
/**
 * Gets config param of installation path.
 *
 * @return array $paths
 */
function get_Paths(){
    //Get param needed to calculate path installation
		$doc_root = apache_getenv('DOCUMENT_ROOT');
		$script_name = apache_getenv('SCRIPT_NAME');
		
		$tmp1 = explode($doc_root, $script_name);
		$tmp2 = explode("/", $tmp1[0]);
		$dir = $tmp2[1];

    //Defining vars and constants for the app
	($doc_root[strlen($doc_root)-1]=='/')?$doc_root=substr($doc_root, 0, strlen($doc_root)-1):null;
	$paths = array();
	$paths['SERVER_NAME'] = _serverName();
	$paths['APP_DIR'] = '/'.$dir;
	$paths['APP_ROOT'] = $doc_root.'/'.$dir;
	$paths['UPLOAD_PATH'] = $doc_root.'/'.$dir.'/archive/';

	return $paths;
}

/**
 * Adapting redirection
 *
 * @return string URL custom
 */
function _serverName(){
	return $_SERVER['SERVER_NAME'];
}

/**
 * Helper function to return the current URL with all params.
 * @return string Current URL with parms
 */
function getLoginURL(){
	
	$params="?";
	foreach($_GET as $key => $value){
		$params.="&$key=$value";
	}
	
	$url = SERVER_NAME.$_SERVER['PHP_SELF'].$params;
	return $url;
}
?>