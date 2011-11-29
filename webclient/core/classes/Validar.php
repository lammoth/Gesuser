<?php
/**
 * Validator system class
 * 
 * @package Core
 * @version 0.1
 * @author 
 * Juan Ramón González Hidalgo
 * 
 * Antonio Irlandés García
 */
 class Validate {
	 
	/**
	 * Constructor
	 */	
	public function __construct(){}

	/**
	 * Dates validation.
	 * 
	 * @param string $date date format "dd/mm/yyyy"
	 */
	public function date($data){

		$valid = false;
	  	//pattern: dd/mm/aaaa
	  	$regexp = "^([[:digit:]]{1,2})/([[:digit:]]{1,2})/([[:digit:]]{2,4})$";
	  	
	  	if(!eregi($regexp, $data))
	  		return false;
	  	else{
	  		//check number range
	  		$date = array();
	  		$date = explode("/", $data);
	  		$day = $date[0];
	  		$month = $date[1];
	  		$year = $date[2];
	  	
	  		if($month<1 || $month>12 || $day<1)
	  			return false;
	  		
	  		switch($month){
	  			case 1:
	  			case 3:
	  			case 5:
	  			case 7:
	  			case 8:
	  			case 10:
	  			case 12:
	  				if($day <= 31)
	  					$valid = true;
	  				break;
	  			case 2:
	  				//check leap year
	  				$leap = false;
	  				
	  				//if number is divisible by 4, 100 y 400, is leap
	  				//if number is divisible by 4, 100 but not by 400, it's not leap
	  				//if number is divisible by 4 and not by 100, it's leap
	  				$r4 = fmod($year, 4);
	  				$r100 = fmod($year, 100);
	  				$r400 = fmod($year, 400);
	  				
	  				if($r4 != 0)
	  					$leap = false;
	  				else if($r100 != 0)
	  					$leap = true;
	  				else if($r100 == 0 && $r400 != 0)
	  					$leap = false;
	  				else if($r100 == 0 && $r400 == 0)
	  					$leap = true;

	  				if($leap){
	  					if($day<=29)
	  						$valid = true;
	  				}
	  	  			else if($day<=28){
	  						$valid = true;
	  	  			}
	  				break;
	  			case 4:
	  			case 6:
	  			case 9:
	  			case 11:
	  				if($day<=30)
	  					$valid = true;
	  				break;
	  		}
	  	}
	  		
	  	return $valid;
	}
	  
 	/**
	 * Generic validation indenticator (int 11 digits)
	 * 
	 * @param integer $data Generic identificator
	 */
	public function id($data){
		$valid = false;
		//8 max digits, 2 min
		$regexp = "^[[:digit:]]{1,11}$";
		 	
		if(is_numeric($data) && eregi($regexp, $data))
			$valid = true;
		 		
		return $valid;  	
	 }
	  
 	/**
     * Search string validation without defined pattern.
	 * 
	 * @param string $data Cadena a validar.
 	 */
 	public function string($data){
 		$valid = false;
 		
 		//Chars allowed
 		$regexp = "[^[:alnum:]áéíóúÁÉÍÓÚ _.,:;ñÑºª@ü()'\"/-]+<>";
 		
	 	if(!eregi($regexp, $data))
	  		$valid = true;
	
	  	if($valid==false)
	  		$this->error=true;
	  		
		return $valid;	
 	}
 	
  	/**
     * Password validation.
	 *
	 * @param string $data Cadena a validar.
 	 */
 	public function passwd($data){
 		$valid = false;

        //Chars alphanumerics
 		$regexp = "[^[:alnum:]]+";
 		
	 	if(!eregi($regexp, $data))
	  		$valid = true;
	
	  	if($valid==false)
	  		$this->error=true;
	  		
		return $valid;	
 	} 	
 	
 	/**
     * Change a date with format dd/mm/yy to timestamp.
	 * 
	 * @param string $date Date format dd/mm/yyyy
	 */
	public function date2timestamp($date){
		$tmp = @explode("/", $date);
		return @mktime(0,0,0,$tmp[1], $tmp[0], $tmp[2]);
	}
	
 	/*
	 * Email data validation
	 * 
	 * @param string $email Email string.
	 */
	public function email($email){
		if(eregi("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", $email)) 
			return true;
		else
			return false;
	
	}
	
	/**
	 * Phone validation
	 * @param integer $data
	 */
	function phone($data){
	  	$valid = false;
	  	//Begins in 9, then 8 digits
	  	$regexp = "^(9|8){1}[0-9]{8}$";
	  	//O is corporative
	  	$regexp_corp = "^[0-9]{6}$";
	  	
	  	if(eregi($regexp, $data) || eregi($regexp_corp, $data))
	  		$valid = true;
	
	  	if($valid==false) $this->error=true;
	  	if($data == '') $valid=true;
		return $valid;  					
	 }
     
	 /**								
 	 * Cellular validation
 	 * @param integer $data
 	 */
 	function cellular($data){
 	  	$valid = false;
	  	//Begins in 6, then 8 digits
	  	$regexp = "^6{1}[0-9]{8}$";
	  	//Also, there're corporative cellulars
	  	$regexp_corp = "^[0-9]{6}$";
	  	
	  	if(eregi($regexp, $data) || eregi($regexp_corp, $data))
	  		$valid = true;
	
	  	if($valid==false) $this->error=true;
		return $valid;  					
 	}
	
	/**
     *
     * Clean not-allowed labels and attrs of allowed labels.
	 * 
	 * @param string $html HTML text to clean.
	 * @param string $labels img,a,p,span ...etc
	 * @param string $attrs href,style,src ...etc
	 * 
	 * @return string $html HTML code clean.
	 */
	public function clean_html($html,$labels,$attrs) {

        //Check if exists a list of allowed labels
		if($labels!=""){
			$labels = str_replace("," , "|" ,$labels);
			$html = ereg_replace("<(/)?(".$labels.")[^>]*>","",$html);
		}
		//Check if exists a list of not-allowed attrs
		if($attrs!=""){
            $attrs = str_replace("," , "|" ,$attrs);
			// then run another pass over the html (twice), removing unwanted attributes
			$html = ereg_replace("<([^>]*)(".$attrs.")=(\"[^\"]*\"|'[^']*'|[^>]+)([^>]*)>","<\\1>",$html);
			$html = ereg_replace("<([^>]*)(".$attrs.")=(\"[^\"]*\"|'[^']*'|[^>]+)([^>]*)>","<\\1>",$html);
		}
		return $html;  
	}

} 
?>
