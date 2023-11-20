<?php
// Sample PHP code
$greeting = "Hello, PHP!";
echo "<h1>$greeting</h1>";

// Simple loop
for ($i = 1; $i <= 5; $i++) {
    echo "Iteration $i<br>";
}

// Associative array
$person = array(
    "name" => "John",
    "age" => 30,
    "city" => "New York"
);

// Accessing array elements
echo "<p>{$person['name']} is {$person['age']} years old and lives in {$person['city']}.</p>";
?>