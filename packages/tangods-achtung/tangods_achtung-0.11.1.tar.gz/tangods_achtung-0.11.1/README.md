Achtung!
========

Achtung is a "PANIC compatible" (not 100%, but the basic features should be the same) Tango alarm device. The idea is that it could be pretty much dropped in as a replacement for `PyAlarm`. This holds as long as you don't rely on more "dynamic" features of PyAlarm. Its main purpose is to use less system resources, as well as being a simpler code base using modern async python and PyTango APIs.


## Main differences to PyAlarm

- Less powerful alarm formulas. Achtung formulas only allows *attributes* (including attribute "properties" like `quality`, `exception` etc) and *variables*, apart from basic logic, arithmetic and the usual math functions. No "dynamic" features. This allows the alarms to be fully parsed on startup - and checked for errors - and then efficiently evaluated during runtime.

- "HTTP consumers" which are basically "web hooks"; sending JSON encoded messages to some HTTP endpoint whenever there is an event (alarm on/off etc). This can be used to integrate with other services. 

- No support for "receivers" (e.g. sending emails), this can be replaced by HTTP consumers.

- Various less common settings.

- Not well documented :)


## Configuration

Generally Achtung is configured the same way as PyAlarm, with the same properties (see [here](https://tango-controls.readthedocs.io/projects/panic/en/latest/PyAlarmUserGuide.html#pyalarm-device-properties)). Achtung does not support all the settings on PyAlarm, however.

Some notable differences:

* `ResetActions` replaces `AlarmResetRecievers` with a mechanism intended to be a bit simpler. It takes lines on the form
    
        my_alarm_tag;write_attribute;sys/tg_test/1/boolean_scalar;1
    
 This means that any time the `my_alarm_tag` alarm is reset, achtung will write a `1` (i.e. "true") to the attribute `boolean_scalar` on device `sys/tg_test/1`. Values/arguments are specified as JSON, so for a string argument, e.g. `"hello"`, a list `[1, 2, 3]`, etc. It's also possible to replace `write_attribute` with `run_command` which works in a similar way, running a device command. For commands that take no argument, just leave out the last `;`, e.g.
 
        my_alarm_tag;run_command;sys/tg_test/1/switchstates
 
* `HttpConsumers` which is a list of HTTP URLs where JSON reports will be POST:ed on alarm status changes. This is intended to replace the `AlarmReceivers` property of PyAlarm and enable integration with e.g. logstash (see below).

* `ReportExtras` is a JSON encoded string containing static key-values that will be added to the JSON reports sent to HTTP consumers.

For the full list of supported properties, see `achtung/achtung.py`.


### Formula syntax

Formulas are how you express the conditions for an alarm to become active. The syntax is based on python syntax but simplified. Achtung does not support the dynamic fandango based features of PyTango.

It's recommended to always separate the parts of your formula with spaces, e.g. `a == 0` instead of `a==0`. It prevents some ambiguity and is also more readable. Longer formulas may use parentheses to clarify grouping.

Some examples of valid, but not very useful formulas:

- `True` This alarm will *always* be active
- `False` Similarly will *never* be active
- `1 != 2`  Always active
- `1 == 2`  Never active

In order to actually be useful, formulas must contain at least one device attribute:

- `sys/tg_test/1/ampli == 3` This alarm is active if the ampli attribute equals 3 exactly.
- `sys/tg_test/1/ampli < 5` ...less than 5.
- `sys/tg_test/1/ampli * 3 >= 10`  Basic math is allowed
- `abs(sys/tg_test/1/ampli) > 10e6`  Also some math functions (see below)
- `sys/tg_test/1/ampli < sys/tg_test/2/ampli` Comparing different attributes
- `sys/tg_test/1/state != ON` Active if device in any other state than ON
- `sys/tg_test/1/boolean_scalar` Directly use a value that is boolean

Hoefully you get the picture. More complex logical expressions are also possible:

- `(sys/tg_test/1/ampli >= 5) and (sys/tg_test/1/ampli < 10)` Attribute value in the given range.
- `not ((sys/tg_test/1/ampli < 2.0 and sys/tg_test/2/ampli < 0) or (sys/tg_test/2/ampli < 6))` Parentheses can be helpful.

More examples:

- `tango://some-other-csdb:10000/sys/tg_test/2/ampli == 0` Access to attributes in a different control system.
- `sys/tg_test/1/ampli.exception` Active if there's a problem accessing the attribute.
- `sys/tg_test/1/ampli.quality != ATTR_VALID` Active if the attribute is not valid, as reported by the device.
- `sys/tg_test/1/ampli.quality == ATTR_ALARM` Active if the attribute's value is outside its min/max_alarm settings.
- `"fault" in sys/tg_test/1/string_scalar` Checking if a substring is present


Operators allowed in formulas (they work like in python):
- `+ - * /`
- `**` power
- `== > < <= >=` for comparison
- `in` for checking for substrings
- `and`, `or`, `not` for logic
- `abs()`, `sin()`, `cos()`, `exp()`, `round()` for rounding to nearest integer

If you have a need for more advanced ways of writing formulas, please get in touch with the software team (or create an "issue" in this repo). 


### Usage with Logstash, Fluentbit, etc.

Achtung can be configured to write alarm reports to a local file, by setting the `ReportLogfile` property. Reports are generated whenever an alarm's status, and appended to the logfile.

The logfile is in ND-JSON (newline delimited) format, where each line is a separate JSON object. This format can easily be ingested by tools like fluentbit, to be sent to a database backend for example. The file is automatically rotated and the settings for rotation can be changed using the `ReportLogfileMaxBytes` and `ReportLogfileBackupCount` properties.

The http consumers feature (see above) is also using a format compatible with Logstash. Here's a logstash configuration example.

```
input {
    http {
        port => 8732
        codec => json
    }
}

filter {
    date {
        match => ["timestamp", "ISO8601"] 
        target => "@timestamp"
    }
}

output {
    elasticsearch {
        hosts => ["<some-es-host>", "..."]
        index => "tango-alarms-%{+YYYY.MM.dd}"
        document_type => "alarm"
    }
}
```
The port can of course be anything, and the output tailored to your needs. This pipeline must also be added to e.g. `/etc/logstash/pipelines.yml`.

Now just remains to add a line to the `HTTPConsumer` property in Achtung: `http://<logstash-host>:8732`.
