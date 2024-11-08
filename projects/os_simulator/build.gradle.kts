plugins {
    kotlin("jvm") version "2.0.0"
}

group = "me.ajh123.os_simulator"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
    implementation("io.github.spair:imgui-java-app:1.87.0")
    implementation("org.pf4j:pf4j:3.12.1")
    annotationProcessor("org.pf4j:pf4j:3.12.1")
}

tasks.test {
    useJUnitPlatform()
}
kotlin {
    jvmToolchain(21)
}