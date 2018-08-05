# Blaze CTF 2018 blazefox

# 0. Set up environment 
1. Follow the [official guide](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions/Simple_Firefox_build/Linux_and_MacOS_build_preparation) to install all dependence required and carry on basic set up 

2. (If you are using ubuntu) You may need update your compiler before process to later steps:

update from source : https://gist.github.com/application2000/73fd6f4bf1be6600a2cf9f56315a2d91

link for gcc library(you may need to revert to the gcc near to the competiton time to reproduce this exploit) : https://ftp.gnu.org/gnu/gcc/

build gcc :

```
wget ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/releases/gcc-7.3.0/gcc-7.3.0.tar.xz
tar xvf gcc-7.3.0.tar.xz
cd gcc-7.3.0/
mkdir build
cd build
./contrib/download_prerequisites
../configure --enable-languages=c,c++ --disable-multilib
make -j 8
sudo make install
gcc --version
```

3.For testing or development of exploit, you just need to build the spidermonkey engine instead of the whole firefox(time consuming and hard to build) For real env, you may use the docker setup provided by the organizer

Step to build the Spidermonkey engine:

Copied from https://bruce30262.github.io/2017/12/15/Learning-browser-exploitation-via-33C3-CTF-feuerfuchs-challenge/

```
cd js/src/
cp configure.in configure && autoconf2.13
mkdir build_DBG.OBJ 
cd build_DBG.OBJ 
../configure --disable-optimize
make # or make -j8
cd ..
```

You should turn off the debug option, since debug options will add tons of assetion to the js-engine,and blocks the exploit


# Reference

1. http://charo-it.hatenablog.jp/entry/2018/05/07/011051

2. https://bpsecblog.wordpress.com/2017/04/27/javascript_engine_array_oob/

3. https://github.com/Jinmo/ctfs/blob/master/2018/blaze/pwn/blazefox.html

4. https://github.com/vakzz/ctfs/blob/master/Blaze2018/blazefox/exploit.html

5. https://bruce30262.github.io/2017/12/15/Learning-browser-exploitation-via-33C3-CTF-feuerfuchs-challenge/
