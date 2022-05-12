This one is an extension and is definitly on another level.  We can solve it but its not easy.

Basically we are trying to do what we saw in the first one but now instead of just calling the string shift with _0x<hexnum>(0x<hexnum>), we now are calling a unique function every time that is taking in 5 parameters, only using one of those and then returning that value after lookup.

> _function _0x1f2eb3(_0x488361, _0x30df6c, _0x8f5ae, _0x43cf02, _0x4ff861) {
> 				return _0xda36(_0x4ff861 - 0x91, _0x8f5ae);
> 			}
> 			function _0x85f0f6(_0x339e15, _0x210275, _0x2e06e7, _0x1b3de5, _0x4d2278) {
> 				return _0xda36(_0x2e06e7 - 0x2dc, _0x210275);
> 			}
> 			function _0x2ececd(_0x29fef2, _0x4ac741, _0x39112d, _0x165f38, _0x7f2131) {
> 				return _0xda36(_0x29fef2 - -0x31f, _0x4ac741);
> 			}
> 			if (_0x85f0f6(0x4b0, 0x4a8, 0x4a5, 0x4ab, 0x4aa) === _0x85f0f6(0x49c, 0x49a, 0x4a5, 0x49e, 0x4b1)) {
> 				if (_0x504b90) {
> 


Before the order was:

After string shifts

Call position shift function > shift > grab string array value > return

Now its:

Call random function with 5 parameters >> Use only one of those and shift >> Call position shift function > shift > grab string array value > return

As we can't really mimic the shift functions, we need to actually use those.

So at this time, the way to solve that is to use regex on the original file, then create two files.  One file with just those string shift functions and another without.  Then paste those function values into the top of our main script so they can be called as is.

(do the normal while string shift, etc)

Lastly, we go back through the obfuscated code, grab the place the strings should be, call the function with half of it and pass the other half as params.

By doing this, we can deob the entire code.  Currently looking for an easier way but not sure anything I have found would be "easier".

More to come.
