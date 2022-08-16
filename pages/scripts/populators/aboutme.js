fetch("./resources/data/aboutme.json")
    .then((response) => response.json())
    .then((data) => {
        const e_root = document.getElementById("aboutme");

        function addEntry(name, value) {
            return createElement({
                node: "div",
                content: [
                    createElement({
                        node: "span",
                        content: name,
                    }),
                    createElement({
                        node: "span",
                        content: value,
                    }),
                ],
            });
        }

        const values = {
            Status: "Student at Quinnipiac University",
            Class: "2024",
            Majors: "Computer Science, Data Science",
            Minors: "Economics",
            "Operating Systems": data["operating systems"].join(", "),
            Uptime: `${data.uptime.y}y ${data.uptime.m}m ${data.uptime.d}d`
        }

        e_root.append(
            createElement({
                node: "div",
                classNames: ["window"],
                content: [
                    createElement({
                        node: "div",
                        classNames: ["title"],
                        content: "littletealeaf@github.io",
                    }),
                    createElement({
                        node: "div",
                        classNames: ["content"],
                        content: [
                            createElement({
                                node: "div",
                                classNames: ["command"],
                                content: [
                                    createElement({
                                        node: "span",
                                        content: "littletealeaf@github.io",
                                    }),
                                    createElement({
                                        node: "span",
                                        content: "neofetch",
                                    }),
                                ],
                            }),
                            createElement({
                                node: "div",
                                classNames: ["neofetch"],
                                content: [
                                    createElement({
                                        node: "img",
                                        src: "./resources/images/misc/profile.webp",
                                    }),
                                    createElement({
                                        node: "div",
                                        classNames: ["details"],
                                        content: [
                                            createElement({
                                                classNames: ["user_title"],
                                                content: ["Thomas Kwashnak"],
                                            }),
                                            createElement({
                                                node: "hr",
                                            }),
                                            ...Object.entries(values).map(([key, value]) =>
                                                createElement({
                                                    node: "div",
                                                    content: [
                                                        createElement({
                                                            node: "span",
                                                            content: key,
                                                        }),
                                                        createElement({
                                                            node: "span",
                                                            content: value,
                                                        }),
                                                    ],
                                                })
                                            ),
                                        ],
                                    }),
                                ],
                            }),
                            createElement({
                                node: "div",
                                classNames: ["command"],
                                content: [
                                    createElement({
                                        node: "span",
                                        content: "littletealeaf@github.io",
                                    }),
                                    createElement({
                                        node: "span",
                                        classNames: ["cursor"],
                                        content: "█",
                                    }),
                                ],
                            }),
                        ],
                    }),
                ],
            })
        );

        // const e_window = document.createElement("div");
        // e_window.classList.add("window");
        // e_root.append(e_window);

        // const e_title = document.createElement("div");
        // e_title.textContent = "tealeaf@littletealeaf.github.io";
        // e_title.classList.add("title");
        // e_window.append(e_title);

        // const e_content = document.createElement("div");
        // e_content.classList.add("content");
        // e_window.append(e_content);

        // const e_cmd_1 = document.createElement("div");
        // e_cmd_1.classList.add("command");
        // const e_cmd_1_prompt = document.createElement("span");
        // e_cmd_1_prompt.innerText = "test";

        // e_window.append(e_cmd_1);
    });
