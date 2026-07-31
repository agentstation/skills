# Editing examples

These examples show the direction of the style. Preserve the facts and voice of
the real task instead of copying the examples mechanically.

## Progress update

Before:

> Great, I have successfully completed the implementation. I am now going to
> proceed with running the test suite to ensure that everything works as
> expected.

After:

> The implementation is complete. I am running the tests now.

## Recommendation

Before:

> It is important to note that using a queue could potentially provide a more
> robust and scalable solution for this use case.

After:

> Use a queue if requests can arrive faster than the worker can process them.
> It limits concurrency and preserves work during traffic spikes.

## Error message

Before:

> An error occurred while processing your upload. Please try again with a valid
> file.

After:

> The upload failed because the file is larger than 10 MB. Choose a smaller
> file and try again.

## Pull-request summary

Before:

> This PR introduces a comprehensive update to the cache layer, enhancing
> performance and improving the overall developer experience.

After:

> This PR adds request coalescing to the cache. Concurrent misses for the same
> key now share one upstream request.

## Uncertainty

Before:

> This should probably fix the issue, although there may potentially be other
> factors involved.

After:

> The trace points to the expired token as the immediate cause. I have not
> ruled out a second failure in the retry path.
