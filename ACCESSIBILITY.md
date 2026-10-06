# Accessibility

<!--
Accessibility matters to Now I See because I want people with different abilities and ways of using technology to be able to use my project. 
The app is especially intended to help people understand and identify colors, including people with color vision differences.

I am responsible for creating, maintaining, and improving this project. 
I want users to be able to use the app and contributors to be able to suggest improvements without unnecessary barriers.

This document explains my accessibility goals, what I expect when making changes to the project, 
how to report accessibility problems, and how I will review and improve accessibility over time.
-->

## Priorities

<!--
I prioritize making Now I See easy to understand and use. I want users to be able to identify colors, explore images, and use the app's main features without unnecessary barriers.
I currently focus on:
Color information: I provide information such as HEX, RGB, and HSL values so users have more than one way to understand a color.
Keyboard use: I aim to make important controls usable with a keyboard where possible.
Screen readers: I aim to use clear labels and descriptions so that important information can be understood by people using screen readers.
Readable content: I want text, labels, buttons, and instructions to be clear and easy to understand.
Clear navigation: I want features to be organized in a predictable way.
Different devices: I want the app to work well across different screen sizes and devices as I continue testing them.
Plain language: I aim to keep instructions and information easy to understand.

I may use WCAG Level AA as an aspirational goal, but I am not claiming that the project currently conforms to that level.
I will only make a conformance claim after completing an accessibility evaluation and documenting the scope, date, method, and evaluator.
-->

## Contributor expectations

<!--
Because I am the sole maintainer of Now I See, I review and make the project's changes myself.

When I add or change a user-facing feature, I will consider whether the change could create an accessibility barrier. 
I will test changes as much as I reasonably can and document relevant accessibility information when needed.

If other people contribute to the project, I ask them to consider accessibility when changing the interface, content, controls, images, or other user-facing features. 
Contributors should explain any accessibility-related testing they performed when submitting a change.

I do not currently use automated accessibility testing or continuous integration checks specifically for accessibility.
I will update this section if I add those tools in the future.
-->

## Reporting accessibility issues

<!--
If you encounter a barrier while using Now I See, please report it through the Issues section of my GitHub repository.

You do not need to disclose a disability when reporting an accessibility problem.

When possible, please include:

What you were trying to do.
The URL where the problem happened.
What you expected to happen.
What actually happened.
Your browser and operating system.
Any assistive technology you were using.
A screenshot or screen recording, if it helps explain the problem. These are optional.

You do not need to know the technical name for an accessibility problem.
Simply explaining what made the project difficult or impossible to use is helpful.
-->

### Severity

<!--
I may assign a severity level to an accessibility issue based on how strongly the problem affects someone's ability to use the project. 
Reporters do not need to choose a severity level, but do have the ability to.

Critical: A barrier prevents someone from completing an important task or accessing a major part of the app.
High: A barrier makes an important feature very difficult to use, although another way to complete the task may exist.
Medium: A barrier makes part of the experience harder to use but does not prevent the main task from being completed.
Low: A barrier causes a minor inconvenience or affects a small part of the experience.

I may change the severity of an issue as I learn more about how it affects users.
-->

### How I respond

<!--
After an accessibility issue is reported, I will review the information provided and determine how the barrier affects the user experience.

When possible, I will:

Acknowledge the reported issue after reviewing it.
Provide updates when the status of the issue changes.
Share a workaround if I know another way to complete the affected task.
Work toward a fix based on the issue's impact and my available time and resources.
Invite the person who reported the issue to test the fix when appropriate.

I cannot promise a specific amount of time for every issue to be resolved. 
The time required may depend on the severity of the problem, how difficult the fix is, and my available resources as the sole maintainer.
-->

## Ownership and maintenance

<!--
I am currently the sole maintainer of Now I See, so I am responsible for accessibility.

My responsibilities include:

Reviewing accessibility issues and feedback.
Considering accessibility when I add or change features.
Prioritizing accessibility problems based on their impact on users.
Working to fix reported accessibility barriers.
Keeping this accessibility information up to date.
Reviewing accessibility when I make major changes or add new features.

I will review accessibility as part of major updates and when accessibility issues are reported.

If someone else takes over maintaining Now I See in the future, 
I will make sure they understand these accessibility responsibilities and have access to this documentation.
-->

## Supported environments

<!--
Now I See is a web-based application. I currently develop and test it primarily on a desktop computer.

Platforms and devices

Desktop: Tested during development.
Mobile devices: Not yet formally evaluated.
Tablets: Not yet formally evaluated.
Browsers
Google Chrome: Tested during development.
Other browsers: Not yet formally evaluated.

I do not currently claim support for browser and assistive-technology combinations that I have not tested.

Input methods

Mouse: Tested during development.
Keyboard: Basic keyboard interaction has been considered, but full keyboard accessibility has not been formally evaluated.
Touch input: Not yet formally evaluated.
Assistive technologies

I have not yet completed formal testing with screen readers or other assistive technologies. 
I therefore do not currently claim full support for specific screen readers, voice-control tools, magnification software, or other assistive technologies.

I will update this section as I test additional platforms, browsers, input methods, and assistive technologies.
-->

## Known limitations

<!--
Accessibility testing for Now I See is still ongoing. I have not completed a full accessibility evaluation, so I cannot currently claim that there are no accessibility barriers.

So far, I have tested the project primarily on a desktop computer using Google Chrome and have tested mouse interaction during development.
Basic keyboard interaction has been considered, but full keyboard accessibility has not been formally evaluated.

Mobile devices, tablets, screen readers, and other assistive technologies have not yet been formally tested.

Because I have not evaluated every environment or way of using the app, users may encounter accessibility barriers that I have not identified yet.

If a user encounters a feature that is difficult to use, they can report it through the project's GitHub Issues.
If I know of another way to complete the affected task, I will provide that workaround when possible.

I will update this section when I identify specific barriers, available workarounds, or tracked accessibility issues.
-->

## Feedback and improvements

<!--
I welcome suggestions for improving the accessibility of Now I See and this accessibility statement.

If you have an idea for improving the app, its design, navigation, instructions, documentation, or accessibility testing, you can suggest it through a GitHub Issue.

If you are currently unable to use a feature or complete a task because of an accessibility barrier,
please use the Reporting accessibility issues process above so I can identify and prioritize the active barrier.

As the sole maintainer, I will review accessibility suggestions and use them to improve Now I See and this statement over time.
-->
