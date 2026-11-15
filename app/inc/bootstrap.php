<?php
declare(strict_types=1);

date_default_timezone_set('Asia/Hong_Kong');
ini_set('display_errors', '1');
error_reporting(E_ALL);
session_start();

const DB_PATH = '/data/app.db';

function db(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

function e(mixed $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}

function current_user(): ?array
{
    if (empty($_SESSION['uid'])) {
        return null;
    }
    $stmt = db()->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->execute([$_SESSION['uid']]);
    return $stmt->fetch() ?: null;
}

function require_login(): array
{
    $user = current_user();
    if (!$user) {
        header('Location: index.php');
        exit;
    }
    return $user;
}

function login_user(array $user): void
{
    session_regenerate_id(true);
    $_SESSION['uid'] = (int) $user['id'];
    setcookie('role', (string) $user['role'], time() + 86400, '/');
}

function flash(string $message): void
{
    $_SESSION['flash'] = $message;
}

function take_flash(): ?string
{
    $message = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $message;
}

function page_start(string $title, ?array $user = null, string $active = ''): void
{
    $home = 'index.php';
    if ($user) {
        $home = 'board.php';
    }
    $boardClass = '';
    if ($active === 'board') {
        $boardClass = 'active';
    }
    $adminClass = '';
    if ($active === 'admin') {
        $adminClass = 'active';
    }

    echo '<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>' . e($title) . ' · CampusConnect</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="' . $home . '">
    <span class="logo">CC</span> CampusConnect
  </a>';

    if ($user) {
        echo '
  <nav>
    <a href="board.php" class="' . $boardClass . '">Phonebook</a>
    <a href="admin.php" class="' . $adminClass . '">Admin</a>
    <span class="who">' . e($user['username']) . ' · ' . e($user['role']) . '</span>
    <a class="btn-small" href="index.php?logout=1">Sign out</a>
  </nav>';
    }

    echo '
</header>
<main class="wrap">';
}

function page_end(): void
{
    echo '
</main>
<footer class="foot">
  CampusConnect demo · All records are fictional · The lab database resets regularly, so changes are temporary.
</footer>
<script src="assets/app.js"></script>
</body>
</html>';
}
