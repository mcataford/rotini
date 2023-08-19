# Identity and ownership

## Problem

The system needs a concept of who the user is to have uploaded files have owners. Owners have permissions on files,
whereas non-owners do not.

## Design

### Storing users and credentials

Taking inspiration from [OWASP's guidance on storing
passwords](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), Argon2 can be used to hash
passwords with a user-specific salt.

#### Comparables

Looking at comparable applications for inspiration about which dependencies to rely on and the standards that exist.

##### Django

[Django](https://docs.djangoproject.com/en/4.2/topics/auth/passwords/) uses PBKDF2 with a SHA256 hash by default, but
allows different hashers to be set by users (incl.
[Argon2](https://docs.djangoproject.com/en/4.2/topics/auth/passwords/)).

Their [Argon2
hasher](https://github.com/django/django/blob/517d3bb4dd17e9c51690c98d747b86a0ed8b2fbf/django/contrib/auth/hashers.py#L374-L473)
[uses](https://github.com/django/django/blob/517d3bb4dd17e9c51690c98d747b86a0ed8b2fbf/setup.cfg#L48-L50) the `argon2-ccfi` [library](https://github.com/hynek/argon2-cffi).

Password hashes are stored as a `VARCHAR(128)` and stores an ASCII string prefixed with the algorithm used and
containing the hash and the salt as a base64 encoded value. This is handled by [the underlying
library](https://github.com/hynek/argon2-cffi/blob/e9473c8f0b8b860bb4369d11f5a605a326255f3f/src/argon2/low_level.py#L53-L118).

The hashed value can be split into parts and `argon2-cffi` can [retrieve the
salt](https://github.com/hynek/argon2-cffi/blob/e9473c8f0b8b860bb4369d11f5a605a326255f3f/src/argon2/_utils.py#L95-L140) for password verification.

##### FastAPI Users

[FastAPI Users](https://github.com/fastapi-users/fastapi-users) uses BCrypt [by
default](https://fastapi-users.github.io/fastapi-users/12.1/configuration/password-hash/) and does not offer
alternatives out-of-the-box without [custom
code](https://fastapi-users.github.io/fastapi-users/12.1/configuration/password-hash/#full-customization) being supplied by adopters.

##### NextCloud

[Nextcloud](https://nextcloud.com) uses Argon [by
default](https://docs.nextcloud.com/server/19/admin_manual/configuration_server/config_sample_php_parameters.html?highlight=htaccess%20rewritebase#hashing).

#### Dependencies

`argon2-cffi` is a good candidate as backing for authentication; being used by Django, it's likely to be closely vetted
for quality.

#### Table design: `users`

|Key|Type|Notes|
|---|---|---|
|`id`|`bigint`|User ID, primary key.|
|`username`|`varchar(64)`|Unique username.|
|`password_hash`|`varchar(128)`|Hashed password, prefixed with algo.|
|`created_at`|`datetime`|UTC datetime of record creation.|
|`password_updated_at`|`datetime`|UTC datetime of the last update to the hashed secret, for renewal tracking.|
|`updated_at`|`datetime`|UTC datetime of last record update.|

The password-storing scheme is largely inspired from Django's, no reason to deviate. Prefixing the algorithm opens the
door to user customization in the future and to changes in algorithm if need be.

Usernames are unique across the table and should be used to refer to the user externally (that way, no leaking of
sequential IDs).

`username` are initially meant to be immutable, but there's no harm in having those be updateable. They do need to be
indexed for searching though.

### Representing ownership

The user table tracks individual users, and the files table tracks file entities. A third table should track the
relationships between the two. This would give entities flexible ownership (i.e. what if a given file could have
multiple owners?).

"Ownership" is too rigid a concept to be represented without needed to be modified a bunch in the future. It might be
best to represent _permissions_ instead such that "owners" have all the permissions on something. This facilitates the
creation of "shared resources" since users that would get files shared to them would just have reduced permissions on
those files. 

Permission representation should be flexible such that we can add different permission types along the way. For that
reason, having a convention such that permissions are stored as a number whose bits represent individual permissions is
probably best.

Storing permissions as `bigint` would provide 64 different bits that can be encoded as different permissions. In
principle, we could represent the number as a string and base64 encode it so that the format is more flexible, but
that's not really necessary (a 64b number should be more than enough to account for all cases of permissions. This also
allows it to be indexed, making different levels of share and ownership searcheable without too much trouble.

Permissions can be updated.

#### Sample permissions

Some permissions that we'd need could be:

- Can read file;
- Can edit file;
- Can delete file;
- Can share file;
- Can copy file;
- ...

#### Table design: `permissions`

|Key|Type|Notes|
|---|---|---|
|`id`|`bigint`|Permission entry ID, primary key.|
|`user_id`|`bigint`|Foreign key to the users table, the user who has the permission set.|
|`file_id`|`uuid`|Foreign key to the file that the permission applies to.|
|`value`|`bigint`|Permission value. The bits represent individual permissions.|
|`created_at`|`datetime`|UTC datetime of record creation.|
|`updated_at`|`datetime`|UTC datetime of last record update.|
