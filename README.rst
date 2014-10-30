``wari``
========
A simple CLI interface to be able to generate keys to setup custom tokens for
OTP engines (like LinOTP). The type of tokens can be TOTP (time based) or HOTP
(event based).


For event based tokens, it can also store the secret and steps so that it can
copy the secret and generated pin to the clipboard with one command::

    $ wari hotp get alfredo
    -> secret with generated pin has been copied to the clipboard

If only PINs are needed, those can also be specified::

    $ wari hotp get alfredo pin
    -> pin copied to the clipboard

To generate an HOTP key::

    $ wari hotp generate
    -> Key in Hex: 943fcaf751d2badc65286adb47f0da258c39c869
    -> Key in b32: SQ74V52R2K5NYZJINLNUP4G2EWGDTSDJ (check: 8)


To generate an HOTP key, store it for a given username with a secret so that
PINs can be generated, all at once::

    $ wari hotp create alfredo
    -> Type secret:
    -> Key in Hex: 8ee378386648afbd62989553934eb69d7db9980a
    -> Key in b32: R3RXQODGJCX32YUYSVJZGTVWTV63TGAK (check: 6)
    -> current step: 3
    -> stored tokens and secret for user: alfredo

We can also update information, such as secret or key::

    $ wari hotp update alfredo secret
    -> Type secret:
    -> stored tokens and secret for user: alfredo

    $ wari hotp update alfredo key
    -> Type key: 8ee378386648afbd62989553934eb69d7db9980a
    -> stored tokens and secret for user: alfredo

    $ wari hotp update alfredo step
    -> Type step: 2
    -> stored tokens and secret for user: alfredo

    $ wari hotp update alfredo b32
    -> Type b32: R3RXQODGJCX32YUYSVJZGTVWTV63TGAK
    -> stored tokens and secret for user: alfredo

Removing a user::

    $ wari hotp remove alfredo


