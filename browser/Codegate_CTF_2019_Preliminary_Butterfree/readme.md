# Codegate CTF 2019 Preliminary Butterfree

Question:

```

Butterfree
Download 2018.11.18 Webkit and Modified 

nc 110.10.147.110 17423 

Download 

Download2


```

Diff the ArrayPrototype.cpp with the one on github , you got these difference :

```
--- 90b70bfa992696d63140ca63fcb035cf/ArrayPrototype.cpp	Tue Jan 15 03:35:52 2019
+++ 90b70bfa992696d63140ca63fcb035cf/ArrayPrototype_org.cpp	Sun Jan 27 17:41:23 2019
@@ -973,7 +973,7 @@
     if (UNLIKELY(speciesResult.first == SpeciesConstructResult::Exception))
         return { };
 
-    bool okToDoFastPath = speciesResult.first == SpeciesConstructResult::FastPath && isJSArray(thisObj) /*&& length == toLength(exec, thisObj)*/;
+    bool okToDoFastPath = speciesResult.first == SpeciesConstructResult::FastPath && isJSArray(thisObj) && length == toLength(exec, thisObj);
     RETURN_IF_EXCEPTION(scope, { });
     if (LIKELY(okToDoFastPath)) {
         if (JSArray* result = asArray(thisObj)->fastSlice(*exec, begin, end - begin))
@@ -1636,4 +1636,4 @@
     globalObject->arraySpeciesWatchpoint().fireAll(vm, lazyDetail);
 }
 
-} // namespace JSC
+} // namespace JSC

```

If you have read saelo 's phrack article (http://www.phrack.org/papers/attacking_javascript_engines.html), you will spot it instantly it is CVE-2016-4622, just go to the phrack article and the git repo (https://github.com/saelo/jscpwn) get the PoC , change the size from 4 to 100 , and set it to return [4] instead of [3]

Embed the addrof and fakeobj to 35c3 webkid 's exploit (https://github.com/saelo/35c3ctf/tree/master/WebKid), change shellcode in order to make it works on linux.

For details, please refer to CVE-2016-4622 and 35c3 webkid 

I can get the shell locally but I tried more than 200 times send the payload to remote service and get the flag in one of the attempt, not sure with the reason.


![alt text](flag.png)
