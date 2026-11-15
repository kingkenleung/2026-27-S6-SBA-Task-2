<?php
require __DIR__ . '/inc/bootstrap.php';

if (isset($_GET['logout'])) {
    $_SESSION = [];
    session_destroy();
    setcookie('role', '', time() - 3600, '/');
    header('Location: index.php');
    exit;
}

if (current_user()) {
    header('Location: board.php');
    exit;
}

$error = '';
$mode = $_POST['action'] ?? $_GET['mode'] ?? 'login';
if (!in_array($mode, ['login', 'register'], true)) {
    $mode = 'login';
}
$username = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($action === 'login') {
        $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
        try {
            $user = db()->query($sql)->fetch();
            if ($user) {
                login_user($user);
                header('Location: board.php');
                exit;
            }
            $error = 'Invalid username or password.';
        } catch (Throwable $ex) {
            $error = 'Database error: ' . $ex->getMessage();
        }
    } elseif ($action === 'register') {
        if ($username === '' || $password === '') {
            $error = 'Username and password are required.';
        } else {
            try {
                // Create the account.
                $stmt = db()->prepare('INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)');
                $stmt->execute([$username, $password, 'student', date('Y-m-d H:i:s')]);
                $stmt = db()->prepare('SELECT * FROM users WHERE username = ?');
                $stmt->execute([$username]);
                login_user($stmt->fetch());
                header('Location: board.php');
                exit;
            } catch (Throwable $ex) {
                $error = 'Registration failed: ' . $ex->getMessage();
            }
        }
    }
}

$loginClass = '';
$registerClass = '';
if ($mode === 'login') {
    $loginClass = 'active';
} else {
    $registerClass = 'active';
}
$loginHidden = 'hidden';
$registerHidden = 'hidden';
if ($mode === 'login') {
    $loginHidden = '';
} else {
    $registerHidden = '';
}

page_start('Sign in');
?>
<section class="auth">
  <div class="hero">
    <span class="eyebrow">S6 ICT · Elective B1</span>
    <h1>Every name.<br>Every number.<br><span>One campus.</span></h1>
    <p class="lead">CampusConnect is the school's new phonebook. Find a classmate, a teacher or the IT help desk in seconds.</p>
    <ul class="ticks">
      <li>Search the whole campus directory</li>
      <li>Add new contacts to the directory</li>
      <li>Works on phone, tablet and desktop</li>
    </ul>
    <p class="hint">Teaching prototype · Fictional records only</p>
  </div>

  <div class="card auth-card">
    <div class="tabs">
      <a href="?mode=login" data-tab="login" class="tab <?php echo $loginClass; ?>">Sign in</a>
      <a href="?mode=register" data-tab="register" class="tab <?php echo $registerClass; ?>">Register</a>
    </div>

    <?php
    if ($error !== '') {
        echo '<div class="alert">' . e($error) . '</div>';
    }
    ?>

    <form id="login-form" data-panel="login" method="post" action="index.php" <?php echo $loginHidden; ?>>
      <input type="hidden" name="action" value="login">
      <label>Username
        <input name="username" value="<?php echo e($username); ?>" autocomplete="username" required>
      </label>
      <label>Password
        <input type="password" name="password" autocomplete="current-password" required>
      </label>
      <button class="btn" type="submit">Sign in</button>
      <p class="small">Student demo account: <code>alice</code> / <code>alice1234</code></p>
    </form>

    <form id="register-form" data-panel="register" method="post" action="index.php" <?php echo $registerHidden; ?>>
      <input type="hidden" name="action" value="register">
      <label>Username
        <input name="username" value="<?php echo e($username); ?>" minlength="3" maxlength="20" autocomplete="username" required>
      </label>
      <label>Password
        <input type="password" name="password" minlength="8" autocomplete="new-password" required>
      </label>
      <label>Confirm password
        <input type="password" name="confirm" minlength="8" autocomplete="new-password" required>
      </label>
      <button class="btn" type="submit">Create account</button>
      <p class="small">New accounts are always students. Ask IT for staff access.</p>
    </form>
  </div>
</section>
<?php page_end(); ?>
