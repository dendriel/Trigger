<?

Class Postgrescom {

	protected $host = "localhost";
	protected $user = "moodle";
	protected $pswd = "moodle";
	protected $dbname = "moodle";
	protected $con = null;
	
	function __construct(){}
	
	function open(){
	    $this->con = pg_connect("host=$this->host user=$this->user password=$this->pswd dbname=$this->dbname");
	    return;
	}
	
	function close(){
	   pg_close($this->con);
	}

/*
 * Returns: 0 if has successful conected to db
 *	    -1 if the conection has failed
*/	
	function statusCon(){

	    if(!$this->con){
		return -1;
	    } else{
		return 0;
	    }
	}

	function query($question) {

		$result = pg_query($this->con, $question);
		if (!$result) {
			return -1;
		} else {
			return $result;
		}
	}
}
?>
