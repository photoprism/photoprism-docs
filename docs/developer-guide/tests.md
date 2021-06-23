# How We Test Our Code

> In any process, obsessing about the wait times will yield greater improvements than practically anything else, for longer than you might think. Automation, simplification, etc. are implementation details of that obsession.<br>— <cite>Dan North</cite>

## Unit Tests ##
### Go ###
To run all unit tests, type `make test` or `go test ./internal/...` in a terminal.

These `make` targets are currently defined for tests:

- `test`: Executes all tests found in a) */internal* with a timeout of 20 min and verbose output and b) *frontend/tests/unit*
- `test-short`: Executes only fast tests found in */internal* with a timeout of 5 min and verbose output
- `test-race`: Same as `test` but with race condition detector (much slower) and higher timeout of 60 min
- `test-codecov`: Same as `test` but creates a coverage log in *coverage.txt* and sends it to [Codecov](https://codecov.io/gh/photoprism/photoprism) (don't use it locally)
- `test-coverage`: Same as `test` but creates a *coverage.txt* file as well as a human-readable report in *coverage.html*; timeout is elevated to 30 min

You can run single tests via `go test -run` in a package directory, e.g. */internal/photoprism*:

```
$ go test -run NameOfTest
```

See [docs](https://golang.org/pkg/testing/#hdr-Subtests_and_Sub_benchmarks) for more info.

#### Test Frameworks ####

Go comes with a cool testing framework, it allows you to write test code using the same language, without needing to learn any library or test engine. [Go advanced testing tips & tricks](https://medium.com/@povilasve/go-advanced-tips-tricks-a872503ac859) contains a lot of useful information. We only import [testify/assert](https://github.com/stretchr/testify/tree/master/assert) to save a few lines for common assertions.

Todo: Use a SQL mock driver to test database interactions, for example https://github.com/DATA-DOG/go-sqlmock.

#### Slow Tests ###

Slow tests and benchmarks can be skipped using the `-short` flag:

```go
func TestTimeConsuming(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping test in short mode.")
    }
    ...
}
```

To execute:

```
go test -short
```
### Javascript ###
To run all javascript unit tests, type `make test-js` in a terminal.


In case you want to run a single test add .only to the test you want to run e.g.:

```javascript
 it.only("should get album id",  () => {
        const values = {
            ID: 5, AlbumName: "Christmas 2019", 
            AlbumSlug: "christmas-2019", AlbumUUID: 66
        };
        const album = new Album(values);
        const result = album.getId();
        assert.equal(result, "66");
    });
```


Test coverage output is saved to *frontend/coverage/html*

#### Test Frameworks ####
To test javascript code we use [mocha](https://mochajs.org/) in combination with [karma](https://karma-runner.github.io/4.0/intro/installation.html), [chai](https://www.chaijs.com/), [sinon](https://sinonjs.org/) and the [karma-istanbul-coverage-reporter](https://github.com/mattlewis92/karma-coverage-istanbul-reporter).

## Acceptance Tests ##

### Download test and config files
Download the following directory and unzip it within your storage directory

``wget https://dl.photoprism.org/qa/acceptance.tar.gz``

### Run tests within the docker container
You can run the tests from within the photoprism container in firefox or chromium.
  
* ```make acceptance-run-chromium```: This executes all tests in headless chromium
  
* ```make acceptance-run-firefox ```: This executes all tests in headless firefox

### Run tests locally
Locally you can run the tests in all supported browsers you have installed.

To run tests locally you need to install testcafe on your machine.
```
npm install -g testcafe
``` 

Start the test-instance (from within the docker container)
```
make acceptance-restart
```

Then you can execute tests with
```
testcafe  firefox,chrome,safari,opera -S \
  -s frontend/tests/acceptance/screenshots frontend/tests/acceptance/
```

You can stop the test-instance using
```
make stop
```

To run tests on remote or mobile devices use
```
testcafe  remote -S \
  -s frontend/tests/acceptance/screenshots frontend/tests/acceptance/
```



### Test Frameworks

Our goal was to implement UI acceptance tests using JavaScript, so that frontend developers are able to run and write them without learning Go.<br>

To make a final decision, we compared  [TestCafe](https://devexpress.github.io/testcafe/), [Cypress](https://www.cypress.io/) and [Nightwatch.js](https://nightwatchjs.org/).
We agreed on using TestCafe as tests were the most stable and pretty fast (because no long timeouts are needed).

|Feature | TestCafe | Cypress | Nightwatch.js|
|------- | -------- | ------- |------------- |
|Supported Browsers Local | Chrome,<br> Firefox,<br> Opera,<br> Safari,<br> Internet Explorer,<br> Microsoft Edge,<br> Google Chrome Canary,<br> Chromium  |Chrome,<br> Chromium,<br> Chrome Canary,<br> Electron | Geckodriver,<br> Chromedriver,<br> Microsoft Webdriver,<br> Safaridriver|
|Supported Browsers Headless | Chrome,<br> Firefox | Electron | Problems running headless |
|Continuous Integration Support | yes | yes | yes|
|Setup | easy via npm | easy via npm | easy via npm |
|Usability | +++ |+++ | ++ |
|Speed (3 tests) |2 min (headless chrome and firefox)<br> 1 min (only chrome headless)<br> 1 min (chrome headed)|5 min (headless electron)<br> 2,5 min (chrome headed)|7 min (chrome headed)<br> headless not working |
|Stability | nice | unstable --> waiting times needed | unstable --> waiting times needed|
|Documentation | +++ | ++ | ++|
|Notes |easy to find elements |easy to find elements |additional library needed to find selectors by text|

Other test libraries and frameworks we currently don't use:
 
- https://codecept.io/
- https://funcunit.com/
- https://www.browserstack.com/
- http://nightwatchjs.org/ (used by [Mozilla's Coral Project](https://github.com/coralproject/talk))
- https://developers.google.com/web/updates/2017/04/headless-chrome
