/*
 * Request utilities.
 *
 * To avoid relying too much on the `fetch` global directly and to facilitate
 * testing, this utility abstracts the logic that makes network requests.
 */

interface RequestOptions {
	method: string
	body: FormData | string
}

interface Response<ResponseSchema> {
	status: number
	json: ResponseSchema
}

type MakeRequestFn<Schema> = (
	url: string,
	opts?: RequestOptions,
) => Promise<Response<Schema>>

/*
 * Wrapper for the logic that makes network requests.
 *
 * This is primarily done to make testing a bit easier, but also to centralize
 * shared concerns across requests (i.e. common headers and such).
 */
async function makeRequest<ResponseSchema>(
	url: string,
	options?: RequestOptions,
): Promise<Response<ResponseSchema>> {
	const response = await fetch(url, { ...(options ?? {}) })

	const json = await response.json()

	return {
		status: response.status,
		json: json,
	}
}

export { RequestOptions, Response, MakeRequestFn }

export default makeRequest
