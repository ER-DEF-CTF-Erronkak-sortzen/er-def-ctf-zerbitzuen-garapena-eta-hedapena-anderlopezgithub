<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
<?php
include 'db.php';

if ($result->num_rows > 0) {
?>    

    <div style="background-color:green; color:white;">
        <h1>Conectado correctamente a la intranet.</h1>
    </div>
    <!--
        $dbusername = "pNce";
        $dbpassword = "ht3Zklyy";
        $dbname = "db";?>
    -->
<?php
} else {
?>
    <div style="background-color:red; color: white;">
        <h1>Error de conexión.</h1>
        <p><a href="index.html">Volver</a></p>
    </div>
<?php
}
$conn->close();
?>  
</body>
</html>
