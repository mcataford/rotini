/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
	preset: "ts-jest",
	testEnvironment: "jsdom",
	setupFilesAfterEnv: ["./tests/testSetup.ts"],
	transform: {
		"^.+\\.(ts|tsx)$": "ts-jest",
	},
}
