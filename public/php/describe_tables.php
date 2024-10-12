<?php
require_once("./utils/Database.php");
require_once("./utils/http_responses.php");

header("Content-Type: application/json");

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
