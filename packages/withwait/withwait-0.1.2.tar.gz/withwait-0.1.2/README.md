# Withwait

A simple utility to ensure that sleep operations always complete, even if an
exception happens within the with statement.

## Usage

```py
from withwait import wait

# Start a 2 second wait timer
with wait(2):
    # These operations happen while the timer is run
    print("Started timer")
    # Even if an error is raised, the timer will always be allowed to complete
    # before the withwait block is closed
    raise Exception("Yikes")

# The exception isn't actually caught so this code won't run
print("This never prints")
```

### Cancelling a timer

If you need to stop the timer during the operation, you can stop it using the
`cancel` method. Normal running will resume from the end of the `with`
statement.

```py
from withwait import wait

with wait(1) as timer:
    # Stop the timer
    timer.cancel()
    # Code after this point in the with statement won't be run

# Program flow resumes normally after
print("Ok")
```

* Different timers can be cancelled separately - if you cancel one timer, all
  other timers will run to completion.

### Aborting a timer

If you don't want to resume normal program flow after the `with` statement,
you can stop the timer using the `abort` method.

```py
from withwait import wait, WithwaitAbort

try:
    with wait(1) as timer:
        # Abort the timer
        timer.abort()
        # Code after this point in the with statement won't be run

    # And code after the with statement won't be run either
    print("Nope")

# We need to catch the exception ourselves
except WithwaitAbort:
    print("Caught")
```

* Arguments can be provided to the `abort` method which will be
  given as arguments to the exception
* Different timers can be aborted separately - if you cancel one timer, all
  other timers will run to completion.

### Aborting all timers

If you want to cancel anything, you can call the `abort_all` method. You can
also raise a `WithwaitAbortAll` exception, which will have the same effect.

```py
from withwait import wait, WithwaitAbortAll

try:
    with wait(1):
        with wait(1):
            with wait(1) as timer:
                # Abort all timers
                timer.abort_all()
except WithwaitAbortAll:
    print("All timers stopped")
```
