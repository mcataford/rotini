import { validateEmail, validatePassword } from "./validation"

describe("Email address format validation", () => {
	it("empty values are not valid", () => {
		expect(validateEmail("")).toBeFalsy()
	})

	it.each`
		scenario               | value
		${"without user"}      | ${"@test.com"}
		${"without @"}         | ${"test.com"}
		${"without domain"}    | ${"me@.com"}
		${"without extension"} | ${"me@domain"}
	`("missing parts make emails invalid ($scenario)", ({ value }) => {
		expect(validateEmail(value)).toBeFalsy()
	})

	it("correctly formatted addresses are valid", () => {
		expect(validateEmail("me@domain.com")).toBeTruthy()
	})
})

describe("Password format validation", () => {
	it("passwords must have at least 8 characters", () => {
		for (let i = 0; i < 8; i++)
			expect(validatePassword("a".repeat(i))).toBeFalsy()
	})

	it("passwords with 8-64 characters are valid", () => {
		for (let i = 8; i <= 64; i++)
			expect(validatePassword("a".repeat(i))).toBeTruthy()
	})

	it("passwords of more than 64 charactrs are invalid", () => {
		expect(validatePassword("a".repeat(65))).toBeFalsy()
	})
})
