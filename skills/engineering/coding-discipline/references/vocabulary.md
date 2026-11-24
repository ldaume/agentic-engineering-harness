# Coding Vocabulary

The terms experienced engineers use to judge a code change, so a review names
the defect the way the field does and points at something a reader can see in
the diff or the test run. Authors and check scripts use it; reviews do not load
it by default. A term is admitted only with a registered source and an
observable marker; evidence and access dates are in `sources.json`. Check:
`exact` (a pattern in the diff or a test run a script can match; none ships
here yet, so no rule ids), `jev` (a typed question), `judge` (a person or model
decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Small change | One self-contained change that does one thing and includes its tests. | [SRC-WRITE-014] | Over about 1000 changed lines, or a few hundred spread over many files; two unrelated goals in one PR. | exact |
| Surgical diff | Every changed line traces to the request. | [SRC-WRITE-014] [SRC-CODE-003] | Reformatted, renamed, or reordered lines outside the requested behavior. | judge |
| Behavior change | A change to what the system does, visible to a user, caller, or test. | [SRC-CODE-003] | An existing test's expected value changed, or a new test asserting new output. | judge |
| Structure change | A change to how the code is arranged with behavior unchanged (a tidying). | [SRC-CODE-003] [SRC-CODE-004] | Moves, renames, extractions, and inlines with no test expectation changed. | judge |
| Mixed change | Structure and behavior changed in the same commit. | [SRC-CODE-003] [SRC-WRITE-014] | One commit that renames or moves code and also changes a test expectation. | judge |
| Refactoring | A structure change made in small behavior-preserving steps. | [SRC-CODE-004] | A commit called a refactoring that changes a test's expected output. | judge |
| Named refactoring | A structure change identified by its catalog name, so the reviewer knows its mechanics. | [SRC-CODE-005] | A structural diff described only as "cleanup" or "improve" instead of Extract Function, Inline Variable, Split Phase. | judge |
| Preparatory refactoring | Make the change easy first, then make the easy change. | [SRC-CODE-006] [SRC-CODE-003] | A feature diff that bends around existing structure with special cases instead of first reshaping it. | judge |
| Presumptive feature | Capability built now for a need guessed at for later (Yagni). | [SRC-CODE-007] | A parameter, option, extension point, or interface with one caller or one implementation and no stated requirement. | judge |
| Code smell | A surface sign that usually points at a deeper design problem. | [SRC-CODE-008] | A finding named by its smell (duplicated code, long parameter list, feature envy) and its location. | judge |
| Duplicated logic | One rule implemented in more than one place, so a fix lands in one and not the others. | [SRC-CODE-009] | A fix applied at one call site while a sibling with the same rule stays unchanged. | judge |
| Reveals intention | Names and structure say what the code is for. | [SRC-CODE-009] [SRC-CODE-010] | A name that needs a comment to explain what it holds or does; `data`, `tmp`, `handle2`. | judge |
| Fewest elements | No class, function, or layer that does not earn its place. | [SRC-CODE-009] | A wrapper, factory, or interface that only forwards to one other element. | judge |
| Deep module | A module whose simple interface hides much functionality. | [SRC-CODE-010] | An interface about as wide as its implementation; callers must know internals to use it. | judge |
| Pass-through method | A method that only forwards its arguments to another with a similar signature. | [SRC-CODE-010] | A function body that is a single call passing its parameters on unchanged. | exact |
| Why comment | A comment that says what the code cannot: the reason, constraint, or non-obvious choice. | [SRC-CODE-010] | A comment restating the next line; a magic number or workaround with no stated reason. | judge |
| Flag argument | A boolean parameter that selects which operation a function performs. | [SRC-CODE-011] | A call with a bare `true` or `false` literal that switches behavior (`book(customer, true)`). | exact |
| Parallel change | An incompatible interface change done as expand, migrate, contract. | [SRC-CODE-012] | A published field, route, or signature removed in the same change that adds its replacement while outside consumers remain. | judge |
| Test list | The behavior variants to cover, written before the first test. | [SRC-CODE-001] | Implementation started with no enumerated cases (basic, edge, failure, unchanged behavior). | judge |
| Red run | The new test seen failing for the expected reason before the code exists. | [SRC-CODE-001] | No failing run recorded before the implementation; a test that never failed. | judge |
| One test at a time | One failing test, made to pass, before the next. | [SRC-CODE-001] | Several new failing tests written at once from the whole test list. | judge |
| Assertion-free test | A test that executes code but checks nothing. | [SRC-CODE-001] | A test body with no assertion, expectation, or verify call. | exact |
| Given When Then | A behavior stated as preconditions, one stimulus, and an observable outcome. | [SRC-CODE-015] | A test with several stimuli, or a Then that asserts internal state rather than an outcome. | judge |
| Structure-insensitive test | A test whose result does not change when only structure changes. | [SRC-CODE-002] | A pure refactoring that forces test edits. | judge |
| Behavioral test | A test whose result changes when behavior changes. | [SRC-CODE-002] | A deliberate behavior break (mutant) that every test still passes. | judge |
| Test double | A stand-in for a production collaborator: dummy, fake, stub, spy, or mock. | [SRC-CODE-013] [SRC-CODE-014] | The unit under test, or an internal collaborator it owns, replaced by a double. | judge |

## Not admitted

- Functions of a few lines as a rule (Clean Code): depth of the interface
  matters, not line count [SRC-CODE-010]; judge deep module and fewest elements.
- "Good code needs no comments": comments carry the why the code cannot
  [SRC-CODE-010].
- "Build it general now, it is cheaper than later": the cost of delay and the
  odds against the guess say otherwise [SRC-CODE-007].
- A refactoring that changes behavior: by definition it is a behavior change
  and is reviewed as one [SRC-CODE-004].
- A fixed line count as the definition of small: smallness is one
  self-contained change, and the reviewer judges size [SRC-WRITE-014].
- "Never mock": doubles are right at awkward or external boundaries
  [SRC-CODE-014]; the defect is mocking the unit under test.
