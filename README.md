pyoctpress
==========

An tool to move your blog to octpresss, now includes wordpress and csdn blog

##How to use

Firt git clone pyoctpress and cd in

    git clone https://github.com/jiang-bo/pyoctpress.git pytoctpress
    cd pyoctpress

For wordpress user, you must export your wordpress blogs with Wordpress-Export-Tool and save into an xml file, e.p. wordpress.xml. Then execute:

    python pyoctpress.py
    [Please input your wordpress.xml file path:] _/your/wordpress/export/file.xml_

For CSDN user, just execute:

    pytn pyoctpress.py -t csdn
    [Please input your CSDN username:]_your csdn username_

Then pyoctpress will generate octpress blog  doc in the current dir.
