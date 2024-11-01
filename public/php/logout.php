<?php
if (isset($_SESSION['user']) and isset($_SESSION['passwd'])) {
    unset($_SESSION['user']);
    unset($_SESSION['passwd']);
    session_destroy();
}

sendResponse(['detail' => 'Logout'], 200);
