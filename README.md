# Sad-Flak
For the Sad-Flak programming language, an unholy fusion of Woefully, and Brain-Flak.


# Docs
so, like brain-flak, you have some nilads and monads. However, control flow does not come from `{...}` loops, instead the control flow comes from woefully, which cannot be explained in one sentence

Nilads evaluate to a value, possibly doing a side effect. Monads evaluate all nilads and monads inside of them, and use the some of their values as the argument, then evaluate as a value

Nilads and monads:

* `()` = evaluates to 1
* `<>` = pop a, push to b (evaluates to popped value)
* `[]` = bool pop a. if the popped value was 0, return 0, otherwise 1.
* `{}` = pop a, evaluate to popped value
* `≤≥` = halt. immediately halts program execution
* `(...)` = push argument to stack a
* `<...>` = still evaluate all inside but evaluate to 0
* `[...]` = evaluates to its argument, multiplied by -1
* `{...}` = pop from b, evaluate to popped value multiplied by argument
* `≤...≥` = jump by argument

What is jump, you may ask?

well, here is where we get to control flow.

there is a command_pointer, or whatever you want to call it. it starts at the first line


    -> ≤()≥(())
       2
       ≤()≥
       ≤≥
    stack:

note the number 2. this evaluates to two blank lines, so this program is identical to

    -> ≤()≥(())


       ≤()≥(()())
       ≤≥
    stack:

We see the line the `->` points at, so we execute that

so, the command `≤()≥` jumps the command_pointer forward by one.

       ≤()≥(())
    ->

       ≤()≥(()())
       ≤≥
    stack: 1
note that the program execution does not immediately jump. so the push one (`(())`) command is still executed.

       ≤()≥(())
    -> \
       v
       ≤()≥(()())
       ≤≥
    stack: 1
when the -> is pointing at a blank line, it instead points to the next non-blank line. also note that the blank lines wrap around the entire program, for purposes of jumping, and when there are blank lines

so we execute the `≤()≥(()())` line

       ≤()≥(())

    -> v
       ≤()≥(()())
       ≤≥
    stack: 1 2

it exectutes the jump, and the `(()())`. the 2 is on the top of stack.

Again, it executes the same line

       ≤()≥(())


    -> ≤()≥(()())
       ≤≥
    stack: 1 2 2

it is still pointing at that line, so once more!

       ≤()≥(())


       ≤()≥(()())
    -> ≤≥
    stack: 1 2 2 2
now the pointer is pointing at the halt command. when we execute the line, the program halts.
then, the stack gets outputted:

    2
    2
    2
    1

so, hopefully you can see how control flow works. Wait, what did you say? "Where are the conditionals". Well, my good friend, there are none.

...

unless you count `[]`, the bool pop command. this command is at the heart of turing completeness, along with it's buddies:

- `{...}` multiplication, used with the bool pop command, you can multiply jump values by things depending on whether a TOS was 0 stack. it also transfers value from the off stack to the on stack

- `<>` this is the pop a to b command, which is needed to keep two stacks working, and also work with multiplication.

and of course

- `≤≥` halting

- `≤...≥` jumping

of course, other commands are needed for TC ness. but these are outstanding ones in control flow.



