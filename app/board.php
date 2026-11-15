<?php
require __DIR__ . '/inc/bootstrap.php';
$user = require_login();

$error = '';
$showForm = false;
$q = $_GET['q'] ?? '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $notes = trim($_POST['notes'] ?? '');

    // Check the required fields.
    if ($name === '' || $phone === '') {
        $error = 'Name and phone number are required.';
        $showForm = true;
    } else {
        $stmt = db()->prepare('INSERT INTO contacts (name, phone, email, notes, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?)');
        $stmt->execute([$name, $phone, $email, $notes, $user['id'], date('Y-m-d H:i:s')]);
        flash('Contact added to the campus phonebook.');
        header('Location: board.php');
        exit;
    }
}

if ($q !== '') {
    $sql = "SELECT c.*, u.username FROM contacts c LEFT JOIN users u ON u.id = c.created_by
            WHERE c.name LIKE '%$q%' OR c.phone LIKE '%$q%' OR c.email LIKE '%$q%' OR c.notes LIKE '%$q%'
            ORDER BY c.name";
    try {
        $contacts = db()->query($sql)->fetchAll();
    } catch (Throwable $ex) {
        $error = 'Database error: ' . $ex->getMessage();
        $contacts = [];
    }
} else {
    $contacts = db()->query('SELECT c.*, u.username FROM contacts c LEFT JOIN users u ON u.id = c.created_by ORDER BY c.name')->fetchAll();
}

$contactCount = count($contacts);
$contactWord = 'contacts';
if ($contactCount === 1) {
    $contactWord = 'contact';
}
$openAttribute = '';
if ($showForm) {
    $openAttribute = 'open';
}

$flash = take_flash();
page_start('Phonebook', $user, 'board');
?>
<section class="page-head">
  <div>
    <span class="eyebrow">Campus directory</span>
    <h1>Phonebook</h1>
    <p class="muted"><?php echo $contactCount; ?> <?php echo $contactWord; ?> · signed in as <strong><?php echo e($user['username']); ?></strong></p>
  </div>
  <form class="search" method="get" action="board.php">
    <input type="search" name="q" value="<?php echo e($q); ?>" placeholder="Search name, phone, email…" aria-label="Search contacts">
    <button class="btn" type="submit">Search</button>
    <?php
    if ($q !== '') {
        echo '<a class="btn ghost" href="board.php">Clear</a>';
    }
    ?>
  </form>
</section>

<?php
if ($flash) {
    echo '<div class="alert good">' . e($flash) . '</div>';
}
if ($error !== '') {
    echo '<div class="alert">' . e($error) . '</div>';
}
if ($q !== '') {
    $matches = count($contacts);
    $matchWord = 'matches';
    if ($matches === 1) {
        $matchWord = 'match';
    }
    echo '<p class="results">Showing results for “<strong>' . $q . '</strong>” — ' . $matches . ' ' . $matchWord . '.</p>';
}
?>

<details class="card add-card" <?php echo $openAttribute; ?>>
  <summary><span class="plus">+</span> Add a contact</summary>
  <form method="post" action="board.php" id="contact-form">
    <div class="grid-2">
      <label>Full name
        <input name="name" maxlength="60" placeholder="e.g. Chan Tai Man" required>
      </label>
      <label>Phone
        <input name="phone" maxlength="20" pattern="[0-9 +()\-]{8,20}" placeholder="9123 4567" required>
      </label>
      <label>Email
        <input type="email" name="email" maxlength="80" placeholder="name@sunrise.edu.hk">
      </label>
      <label>Notes
        <textarea id="notes" name="notes" maxlength="200" rows="3" placeholder="Class, room, office hours…"></textarea>
        <span class="counter" id="notes-count">0/200</span>
      </label>
    </div>
    <div class="form-actions">
      <button class="btn" type="submit">Save contact</button>
      <span class="small">Shared with everyone in the directory.</span>
    </div>
  </form>
</details>

<div class="card table-card">
  <table>
    <thead>
      <tr><th>Name</th><th>Phone</th><th>Email</th><th>Notes</th><th>Added by</th></tr>
    </thead>
    <tbody>
    <?php
    foreach ($contacts as $c) {
        echo '<tr>
        <td class="strong">' . $c['name'] . '</td>
        <td>' . $c['phone'] . '</td>
        <td><a href="mailto:' . $c['email'] . '">' . $c['email'] . '</a></td>
        <td class="notes">' . $c['notes'] . '</td>
        <td class="muted">' . e($c['username'] ?? 'system') . '</td>
      </tr>';
    }
    if (!$contacts) {
        echo '<tr><td colspan="5" class="empty">No contacts found. Try a different search.</td></tr>';
    }
    ?>
    </tbody>
  </table>
</div>
<?php page_end(); ?>
