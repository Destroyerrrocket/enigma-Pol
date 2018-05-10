#!/bin/sh

cat testdoc.txt | gpg -ea -vv -R polmarcetsarda@gmail.com > testdoc.txt.asc
cat testdoc.txt.asc | gpg -d -vv > testdoc.txt
cat > template <<EOF
     %echo Generating a basic OpenPGP key
     Key-Type: default
     Key-Length: 4096
     Subkey-Type: default
     Subkey-Length: 4096
     Name-Real: Test Boy
     Name-Comment: Sóc una proba simpàtica
     Name-Email: test@encriptador.pol
     Expire-Date: 0
     Passphrase: contra_segura
     # Do a commit here, so that we can later print "done" :-)
     %commit
     %echo done
EOF
gpg --batch --full-gen-key template
