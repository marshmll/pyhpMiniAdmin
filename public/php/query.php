<?php
require_once("./utils/Database.php");
require_once("./utils/http_responses.php");

header("Content-Type: application/json");

$body = json_decode(file_get_contents("php://input"), true);
session_start();

if (!isset($body["query"]))
    sendResponse(['detail' => 'Query não recebida.'], 400);

try {
    $result = Database::query($body["query"], [], true);

    if (gettype($result) == "boolean") {
        if ($result)
            sendResponse([['detail' => 'A operação foi realizada com sucesso']]);
        else
            sendResponse([['detail' => 'A operação falhou']]);
    }
    sendResponse($result);
} catch (Exception $e) {
    sendResponse([['detail' => $e->getMessage()]]);
}
