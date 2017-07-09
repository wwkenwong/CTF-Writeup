#polictf2017 Status box-120


```

This Box memorizes a statuses sequence composed by a current status and all the previous ones. It already contains a small sequence of 

statuses, but you can show only the current one. You can set a new status, modify the current one or delete it: in this way the box goes 

back to the previous one in the sequence. The box can keep track of maximum 200 statuses. It seems just to work fine, even though we 

didn't test it a lot...;

nc statusbox.chall.polictf.it 31337




```


呢條其實唔難,如果有睇題目 -_-

```
StatusBox started! This Box memorizes a statuses
sequence composed by a current status and all the previous ones.
It already contains a small sequence of statuses, but you can show
only the current one.
You can set a new status, modify the current one or delete it: in this way
the box goes back to the previous one in the sequence.
The box can keep track of maximum 200 statuses.
It seems just to work fine, even though we didn't test it a lot...
CURRENT STATUS:
This is the status set as default current status, change it!


Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)


Your choice was: 
````


