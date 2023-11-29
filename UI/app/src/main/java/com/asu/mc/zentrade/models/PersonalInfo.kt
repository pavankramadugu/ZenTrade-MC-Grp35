package com.asu.mc.zentrade.models

import java.io.Serializable

data class PersonalInfo(
    var firstName: String = "",
    var lastName: String = "",
    var age: Int = 0,
    var email: String = "",
    var phoneNumber: String = "",
    var sex: String = "",
    var countries: MutableList<String> = mutableListOf(),
    var instruments: MutableList<String> = mutableListOf(),
    var appetite: String = "",
    var stress: String = "",
    var frequency: String = ""
) : Serializable
