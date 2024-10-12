<?php
function sendResponse($response = [], $status = 200)
{
    http_response_code($status);
    echo json_encode($response);
    die();
}