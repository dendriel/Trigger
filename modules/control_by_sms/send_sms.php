<?php
$host = "127.0.0.1";
$port = 3435;
$timeout = 3;
?>
<html>

<head>
<title>SENAS</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<link rel="stylesheet" type="text/css" href="layout.css">
</head>

<body>

<h1>SENAS</h1>

<h2><u>Sistema de Envio Autom&aacute;tico de SMS</u></h2>
<h3>Enviar SMS</h3>

<div align="center">
   <table>

    <form name="send_sms" action="send_sms.php" method="post">

<tr><!--start of line 1-->

      <tr>  <!--start-->
         <td><div class="txt_inp">Origem:<input type="text" name="orig" maxlength=8 value="<?php echo $_POST['orig'];?>"></div></td>
      </tr> <!--end-->

      <tr> <!--start-->
         <td><div class="txt_inp">Data/Hora:<input type="text" name="datetime" maxlength=12 value="<?php echo $_POST['datetime']; ?>"/></div></td>
      </tr><!--end-->
        <tr><!--start-->
	  <td><div class="txt"><br />Mensagem:<div style:"float:right"><textarea rows="8" cols="19" name="msg" maxlength=149><?php echo $_POST['msg'];?></textarea> <br />M&aacute;x.149 caracteres</div></div><br /></td>
        </tr><!--end-->
	<tr>
<?php


#echo "mount: ",$_POST['mount_dest'];
#echo "dest: ",$_POST['dest_num'];

	echo "<td>Destinos: <input type=\"text\" name=\"mount\" size=1 readonly=\"readonly\" value=\"";

	if($_POST['dest_num'] == null )
		$mount_dest = $_POST['mount'];
	else
		$mount_dest = $_POST['dest_num'];
	echo $mount_dest;

	echo "\"></td>";

	for($i = 0; $i < $mount_dest; $i++) {
		echo "
      <tr>  <!--start-->
         <td><div class=\"txt_inp\">Destino:<input type=\"text\" name=\"dest$i\" maxlength=12></div></td>

	   <div class=\"txt\"><!--Operadora:-->

	    <tr>
	      <td class=\"txt_rad\"><input type=\"radio\" name=\"oper$i\" checked=\"yes\" value=\"0\" />VIVO
	      <input type=\"radio\" name=\"oper$i\" value=\"1\" />OI
	      <input type=\"radio\" name=\"oper$i\" value=\"2\" />CLARO
	      <input type=\"radio\" name=\"oper$i\" value=\"3\" />TIM</td>
	    </tr>

	   </div>

        </tr> <!--end-->
	";
	}
?>
</tr>
        <tr><!--start-->
          <td><input type="submit" value="Enviar" style="float:right"/></td>
        </tr><!--end-->

</tr>
    </form>
   </table>
</div>

<?php

# Retrieving fields content #
$orig = $_POST['orig'];
$datetime = $_POST['datetime'];
$oper = $_POST['oper'];
$msg = $_POST['msg'];

# Checking if was filled #
$len_orig = strlen($orig);
#$len_dest = strlen($dest);
$len_datetime = strlen($datetime);
$len_msg = strlen($msg);

	
	if ($len_datetime < 12) {
		?><div class="error"><?php echo "Campo Data/Hora de envio incompleto."; ?></div><?php
		return;
	}
	else if ($len_msg == 0) {
		?><div class="error"><?php echo "Voc&ecirc; n&atilde;o pode enviar uma mensagem vazia."; ?></div><?php
		return;
	}

	$part = "";
	for($i = 0; $i < $mount_dest; $i++) {
		$index = "dest$i";
		$part = $part . "\PART$i:$_POST[$index]/PART$i";
	}
	$info = "";
	for($i = 0; $i < $mount_dest; $i++) {
		$index = "oper$i";
		$info = $info . "\INFO$i:$_POST[$index]/INFO$i";
	}

	$stream = fsockopen($host, $port, $errno, $errstr, $timeout);
	stream_set_timeout($stream, $timeout);
	if ($stream == Null) {
		?><div class="error"><?php echo "O sistema est&aacute; indispon&iacute;vel no momento."; ?></div><?php
	}
	else {
		$package = "\ID:100/ID
                            \CMD:send_sms/CMD
                            \FROM:$orig/FROM
                            \CONTENT:$msg/CONTENT
                            \HOWMANY:$mount_dest/HOWMANY
                            \BLOW:$datetime/BLOW
                            \DATA:
                               $part
			       $info
                            /DATA";

		fputs($stream, $package); 
		$answer = fgets($stream);
		echo $package;
		if ($answer == "OK") {
			?><div class="txt"><?php echo "SMS agendado com sucesso!";?></div><?php
		}
		else if ($answer == "ERROR") {
			?><div class="error"><?php echo "Erro do sistema."; ?></div><?php

		}
		else if ($answer == "NOTFOUND") {
			?><div class="error"><?php echo "Faltam dados na requisi&ccedil;&atilde;o."; ?></div><?php
		}
		else if ($answer == "INVALID") {
			?><div class="error"><?php echo "Data/Tempo inv&aacute;lido."; ?></div><?php
		}
		else {
			?><div class="error"><?php echo "Resposta desconhecida do servidor."; ?></div><?php
		}
	}

// No, we DON'T need javascript =/ //
?>

</body>
</html>
