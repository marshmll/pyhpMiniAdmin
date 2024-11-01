<?php
require_once("./utils/Database.php");
require_once("./utils/http_responses.php");

header("Content-Type: application/json");
session_start();

if (isset($_SESSION['user']) and isset($_SESSION['passwd'])) {
    unset($_SESSION['user']);
    unset($_SESSION['passwd']);
    session_destroy();
}

if (!isset($_POST['user']) or !isset($_POST['passwd']))
    sendResponse(['detail' => "user ou passwd não foram recebidos."], 422);

try {
    $conn = new mysqli('mysql', $_POST['user'], $_POST['passwd'], 'classroom');
    $conn->close();

    $_SESSION['user'] = $_POST['user'];
    $_SESSION['passwd'] = $_POST['passwd'];
} catch (Exception $e) {
    sendResponse(['detail' => 'Não foi possível se conectar ao banco: ' . $e->getMessage()], 401);
}

sendResponse([
    'detail' => "Usuário logado com sucesso."
]);
