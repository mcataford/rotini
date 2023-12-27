/*
 * Validates email address formats.
 *
 * Addresses are expected of the format:
 *   user@domain.ext
 */
function validateEmail(value: string | undefined): boolean {
	return Boolean(
		value &&
			(
				value.match(
					/^[A-Za-z0-9.-_]+@[A-Za-z0-9-_]+(\.[A-Za-z0-9-_]+)*\.[a-zA-Z]+$/g,
				) ?? []
			).length === 1,
	)
}

/*
 * Validates password formats.
 *
 * Passwords are enforced to have:
 *  - Between 8 and 64 characters
 */
function validatePassword(value: string | undefined): boolean {
	if (!value || value.length < 8 || value.length > 64) return false

	return true
}

export { validateEmail, validatePassword }
