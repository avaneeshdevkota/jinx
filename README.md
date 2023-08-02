# Jinx

Jinx is a Python tree-walk interpreter for <a href = "http://journal.stuffwithstuff.com"> Bob Nystrom</a>'s Lox programming language from the first half of the book <a href = "http://www.craftinginterpreters.com"> Crafting Interpreters</a>. While the interpreter generally works, there are undoubtedly bugs present.

While Bob writes his tree-walk interpreter in Java, I chose to write mine in Python as I am unfamiliar with Java and wanted a more mindful learning experience than simply copy-pasting Java code.

## Installing and Running

<ul>
<li> Clone this repo.</li>
<li> <code> python3 pjinx/Jinx.py </code> to use Jinx in REPL mode.</li>
<li> <code> python3 pjinx/Jinx.py path/to/script </code> to execute a script.</li>

<br>

## The Jinx Language
<br>

<ul>
<li>Hello World!<br><br>
<pre> print("Hello World!"); <strong>OR</strong> print "Hello World!";</pre></li>

<li>End statements with ';'<br><br>
<pre> Don't let a semicolon ruin your day.</pre></li>

<li>Comment with '#'<br><br>
<pre> # This is a comment. </pre></li>

<li>Dynamic Typing<br><br>
<pre> var a = "this is a string"; <br> a = 100; # Now its a number! </pre></li>

<li>Automatic Memory Management<br><br>
<pre> Jinx relies on Python's Garbage Collector for all its Memory management needs. </pre></li>

<li>Data Types<br><br>
<ul>
<li>Booleans <br><br>
<pre>True; # This is true.<br>False; # This is not true.</pre></li>

<li>Numbers <br><br>
<pre>Currently, Jinx only supports floating point numbers.</pre></li>

<li>Strings <br><br>
<pre>We enclose strings in double quotes. "This is a string". 'This is not'.</pre></li>

<li>Nil <br><br>
<pre>The same as good old None. Or null.</pre></li>
</ul>

<li>Expressions<br><br>
<ul>
<li>Addition <br><br>
<pre>print(1 + 2); # 3 <br>print("one" + "two"); # "onetwo" </pre></li>

<li>Subtraction <br><br>
<pre>print(2 - 1); # 1</pre></li>

<li>Multiplication <br><br>
<pre>print(2 * 3); # 6 <br>print(2 * "three"); # "threethree" <br>print("two" * 3); #"twotwotwo"</pre></li>

<li>Division <br><br>
<pre>print(5 / 2); # 2.5</pre></li>

<li>Negation <br><br>
<pre>print(-5); # -5</pre></li>

<li>Less than <br><br>
<pre>print(5 < 2); # False</pre></li>

<li>Less than or equal <br><br>
<pre>print(5 <= 2); # False</pre></li>

<li>Greater than <br><br>
<pre>print(5 > 2); # True</pre></li>

<li>Greater than or equal <br><br>
<pre>print(5 <= 2); # True</pre></li>

<li>Equality <br><br>
<pre>print(1 == 2); # False <br>print("one" != "two"); # True <br>print(1 == "one"); # False</pre></li>

<li>Not <br><br>
<pre>print(!true); # False <br>print(!false); # True</pre></li>

<li>And <br><br>
<pre>print(true and false); # False <br>print(true and true); # True <br>print(false and false); # False</pre></li>

<li>Or <br><br>
<pre>print(true or false); # True <br>print(true or true); # True <br>print(false or false); # False</pre></li>

<li>Precendence and Grouping <br><br>
<pre>The same precedence and associativity as in C. () can be used to group if the result isn't what you wanted.</pre></li>

</ul>

<li>Statements<br><br>
<ul>
<li>Print <br><br>
<pre>print("Just about anything.");</pre></li>

<li>Blocks <br><br>
<pre>You can wrap a series of statments in a block. <br><br>{<br>   print("one");<br>   print("two");<br>}</pre></li>
</ul>

<li>Control Flow<br><br>
<ul>
<li>If <br><br>
<pre>if (condition) {<br>   print("ok.");<br>} else {<br>    print("not ok.")<br>}</pre></li>

<li>While <br><br>
<pre>while (condition) {<br>   print("do something.");<br>}</pre></li>


<li>For <br><br>
<pre>for (initializer; condition; increment) {<br>   print("do something.");<br>}</pre></li>
</ul>

<li>Functions<br><br>
<ul>
<li>Defining Functions<br><br>
<pre>fun printSum(a, b) {<br>   print(a + b);<br>}</pre></li>

<li>Calling Functions<br><br>
<pre>var a = 5; <br>var b = 6; <br>printSum(a, b); #11</pre></li>

</ul>

<li>Classes<br><br>
<ul>
<li>Defining Classes<br><br>
<pre>class Code {<br><br>  scratchHead() {<br>    print("What is this?");<br>  }<br><br>  blame(someone) {<br>    print("I bet" + someone + " wrote this.");<br>  }<br>}</pre></li>

<li>Creating Instances<br><br>
<pre>var dailyLife = Code(); <br>dailyLife.scratchHead(); # "What is this?"<br>dailyLife.blame("Avaneesh"); # "I bet Avaneesh wrote this."</pre></li>

<li>Inheritance<br><br>
<pre>class Debug < Code {<br>  cry() {<br>    print("Tears are salty.");<br>  }<br>}</pre></li>

</ul>

<li>Standard Library<br><br>
<ul>
<li>Print</li>
<li>Input</li>
<li>Len</li>
<li>Clock</li>
<li>toString</li>
</ul>
</ul>


