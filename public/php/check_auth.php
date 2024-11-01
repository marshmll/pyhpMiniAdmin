<?php
require_once("./utils/http_responses.php");

session_start();

if (!isset($_SESSION['user']) or !isset($_SESSION['passwd'])) {
    sendResponse(['detail' => 'Não autenticado.'], 401);
} else {
    sendResponse(['detail' => 'Autenticado.'], 200);
}
