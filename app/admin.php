<?php
require __DIR__ . '/inc/bootstrap.php';

$secret = trim((string) @file_get_contents(__DIR__ . '/secret.key'));
$token = (string) ($_GET['token'] ?? '');
$cookieAdmin = (($_COOKIE['role'] ?? '') === 'admin');
$tokenAdmin = $token !== '' && hash_equals($secret, $token);
$isAdmin = $cookieAdmin || $tokenAdmin;

if (!$isAdmin) {
    http_response_code(403);
    page_start('Access denied', current_user());
    ?>
    <section class="card narrow">
      <span class="eyebrow">403 · Staff only</span>
      <h1>Access denied</h1>
      <p class="muted">This area is for staff administrators. If you believe you should have access, contact the IT Help Desk.</p>
      <a class="btn" href="index.php">Back to sign in</a>
    </section>
    <?php
    page_end();
    exit;
}

$redirect = 'admin.php' . ($tokenAdmin ? '?token=' . urlencode($token) : '');

if (isset($_GET['delete'])) {
    $stmt = db()->prepare('DELETE FROM contacts WHERE id = ?');
    $stmt->execute([(int) $_GET['delete']]);
    header('Location: ' . $redirect);
    exit;
}

$users = db()->query('SELECT * FROM users ORDER BY id')->fetchAll();
$contacts = db()->query('SELECT c.*, u.username FROM contacts c LEFT JOIN users u ON u.id = c.created_by ORDER BY c.id DESC')->fetchAll();
$lastRestore = trim((string) @file_get_contents('/data/restore.log'));
$querySuffix = $tokenAdmin ? '&token=' . urlencode($token) : '';
$accessMessage = 'Access granted with an administrator cookie.';
if ($tokenAdmin) {
    $accessMessage = 'Access granted with an API token.';
}
$lastResetText = $lastRestore;
if ($lastResetText === '') {
    $lastResetText = 'not recorded';
}
$serverSoftware = $_SERVER['SERVER_SOFTWARE'] ?? 'unknown';

page_start('Admin console', current_user(), 'admin');
?>
<section class="page-head">
  <div>
    <span class="eyebrow">Staff only</span>
    <h1>Admin console</h1>
    <p class="muted"><?php echo $accessMessage; ?></p>
  </div>
  <a class="btn ghost" href="board.php">← Phonebook</a>
</section>

<div class="stats">
  <div class="stat"><span>Users</span><strong><?php echo count($users); ?></strong></div>
  <div class="stat"><span>Contacts</span><strong><?php echo count($contacts); ?></strong></div>
  <div class="stat"><span>PHP</span><strong><?php echo PHP_VERSION; ?></strong></div>
  <div class="stat"><span>Last reset</span><strong class="small-strong"><?php echo e($lastResetText); ?></strong></div>
</div>

<div class="card table-card">
  <h2>User accounts</h2>
  <p class="muted">Account details for staff reference.</p>
  <table>
    <thead><tr><th>ID</th><th>Username</th><th>Password</th><th>Role</th><th>Created</th></tr></thead>
    <tbody>
    <?php
    foreach ($users as $u) {
        echo '<tr>
        <td>' . (int) $u['id'] . '</td>
        <td class="strong">' . e($u['username']) . '</td>
        <td><code>' . e($u['password']) . '</code></td>
        <td><span class="badge">' . e($u['role']) . '</span></td>
        <td class="muted">' . e($u['created_at']) . '</td>
      </tr>';
    }
    ?>
    </tbody>
  </table>
</div>

<div class="card table-card">
  <h2>Directory contacts</h2>
  <table>
    <thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Notes</th><th>Added by</th><th></th></tr></thead>
    <tbody>
    <?php
    foreach ($contacts as $c) {
        echo '<tr>
        <td>' . (int) $c['id'] . '</td>
        <td class="strong">' . $c['name'] . '</td>
        <td>' . $c['phone'] . '</td>
        <td>' . $c['email'] . '</td>
        <td class="notes">' . $c['notes'] . '</td>
        <td class="muted">' . e($c['username'] ?? 'system') . '</td>
        <td><a class="link-danger" href="admin.php?delete=' . (int) $c['id'] . $querySuffix . '" data-confirm="Delete this contact?">Delete</a></td>
      </tr>';
    }
    if (!$contacts) {
        echo '<tr><td colspan="7" class="empty">No contacts in the directory.</td></tr>';
    }
    ?>
    </tbody>
  </table>
</div>

<details class="card">
  <summary>Server information</summary>
  <pre>Database   : <?php echo DB_PATH; ?>

PHP        : <?php echo PHP_VERSION; ?> (<?php echo PHP_OS; ?>)
Web server : <?php echo e($serverSoftware); ?>
Host       : <?php echo e(php_uname()); ?>
Last reset : <?php echo e($lastResetText); ?></pre>
</details>
<?php page_end(); ?>
