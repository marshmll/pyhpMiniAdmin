<?php
require_once("./utils/Database.php");
require_once("./utils/http_responses.php");

header("Content-Type: application/json");
session_start();

if (!isset($_SESSION['user']) or !isset($_SESSION['passwd'])) {
    http_response_code(401);
    die();
}

$result = Database::query("SHOW TABLES");

$tables = [];

foreach ($result as $table)
    array_push($tables, $table["Tables_in_classroom"]);

$descriptions = [];

foreach ($tables as $table) {
    $description = Database::query("DESCRIBE %s", [$table]);
    $descriptions += [$table => $description];
}


sendResponse($descriptions);
