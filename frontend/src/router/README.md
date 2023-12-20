# Frontend routing

Frontend routing is handled by two components: `Router` and `Route`.

```tsx
<Router>
    <Route path="/">
        <ComponentA/>
    </Route>
    <Route path="/:itemId">
        <ComponentB/>
    </Route>
</Router>
```

The `Router` acts as a wrapper for any number of `Route` components that define a path and children to be rendered if
the browser location matches the path pattern. Parameters can be inserted in patterns by using the `:<name>` syntax
(i.e. `/item/:itemId`).

## Rendering

The `Router` expects exactly one `Route` to match the browser location at any given time. If less or more than one
match, an error is thrown and can be handled to display an error fallback.
