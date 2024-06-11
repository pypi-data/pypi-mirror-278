<?php

$options = getopt('h', array(
    'help',
    'path:',
    'name:',
    'value:',
));

$help = isset($options['h']) or isset($options['help']);
$path = isset($options['path']) ? $options['path'] : null;
$name = isset($options['name']) ? $options['name'] : null;
$value = isset($options['value']) ? $options['value'] : null;

if ($help or !$path or !$name or !$value) {
    $script = basename($argv[0]);
    echo "Usage:  $script --path FANNIE_CONFIG_PATH --name SETTING_NAME --value SETTING_VALUE\n";
    exit($help ? 0 : 1);
}

if (!is_file(realpath($path))) {
    echo "Config file does not exist: $path\n";
    exit(2);
}
$path = realpath($path);

// convert value from JSON to PHP
$value = json_decode($value);
if (gettype($value) == 'string') {
    $value = "'$value'";
} else {
    echo gettype($value) . " data type not supported: " . print_r($value, true);
    exit(2);
}

// invoke native CORE logic to update config file
require(dirname($path) . '/install/util.php');
confset($name, $value);

?>
