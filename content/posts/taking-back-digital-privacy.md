+++
date = "2021-04-24T13:30:00Z"
title = "A Case Study of Taking Back Digital Privacy"
tags = ["technology", "privacy"]
+++

This article is about a case in which a person taking back their digital privacy. It may help you if you or your friends are in a similar situation. However, you should seriously consider the possibility that the possessive persons would physically harm others when they are denied.

# Background

Alex lived with Billy. Alex was quite a tech person but Billy was totally not. It was natural for Billy to rely on Alex on all technological problems. Alex set up all Billy's digital accounts and smartphones. It seemed to be fine until Alex's possession over Billy surfaced. Alex spied on Billy's emails, Whatsapp, and iCloud photos.

Billy decided to take back their privacy. Billy and their friend, friend C, started to do so but encountered a roadblock. They consulted me. During the discussion, I discovered that their original plan would not work. Alex could regain control in no time. It was actually not straight forward for Billy.

# Situation

The challenges were

1. Alex had total control over Billy's accounts.
1. Alex and Billy lived together.
1. Alex had a tremendous advantage of technological knowledge over Billy.
1. Billy needed to write down all account passwords in a notebook to remember them.
1. Billy generally required face-to-face assistance on computer related issues but was overseas and far away from friend C and me.
1. Billy did not have a trustable computer which was confidently free of spywares.

After a more in-depth discussion, I confirmed a set of fulfilled prerequisites just enough to take back the privacy

1. Billy had been locking the phone with a password only.
1. They were able to physically secure the phone.
1. They had a nearby helping friend, friend D, who could follow my instructions with only remote assistance.
1. friend D had a PC.

# Outline of the Plan

A written plan was necessary. The process involved many steps which were easy to miss. Some were even needed to be verified first. The process would be in a hurry too. Taking back the accounts would trigger the service providers to send emails to the registered email address. It was nice to have a PC and a stable and high-speed internet connection so we could act efficiently but the process would still take several hours. If Alex checked Billy's emails during the process, they could simply change the passwords to block us.

The outline of the process was

1. to make a backup.
1. to take back as many accounts as possible.
1. to migrate the forever insecure accounts.
1. to strengthen up the security setting of the phone.
1. to educate Billy on privacy protection.
1. to do routine security examinations.
 
## Making Backups

Billy used an iPhone. The only backup was on iCloud. It was unsafe to rely on using iCloud to back up while changing it. Using a PC to back up the phone gave an isolated copy.

You do not need to delete the backup immediately if you trust your helpers or computers. You may wait for a month to see if there is any missing data caused by the migration.

## Taking Back the Accounts

It involved removing signed in devices, changing the passwords, the recovery settings, and strengthening up the security settings. Changing the recovery and security settings would prevent Alex from taking control of the accounts again. I chose SMS as the 2-factor authentication here. I generally discourage anyone to do so because SMS was barely better than nothing. You should use an authenticator. Consider the complications for Billy to adopt them, especially in this stressful situation, it was acceptable to settle on SMS for the time being.

If you do not know the passwords, you may try to recover them from your computers. They may be stored in password managers in your browsers or OSes. If you do not have all your passwords, it worths trying existing passwords from other accounts.

## Migration of Insecure Accounts

Replacement accounts would be needed for the accounts if they could not be taken control of. It would need data migration. That of iCloud was the most dangerous. One wrong step would wipe the data. This was the reason to have an isolated backup.

## Strengthening up the Security Setting of the Phone

The phone, having access and the ability to grant new access to the accounts, would be an attractive target for Alex to attack. Existing iCloud backup and jailbreaks should be removed. All biometric authentications, e.g. face unlock and fingerprint unlock, should be disabled. I confirmed there was no iCloud locks on the phone so there was no need to buy a new phone. I also confirmed that Billy was the solo legal owner of the phone number. Alex could not get a new SIM card for the phone number from the telecom provider without breaking some serious law. The SIM card was removable so a SIM lock was required to prevent Alex from simply loading Billy's SIM into another phone. SMS previews on the lock screen should be disabled to prevent Alex from peeking the codes for 2-factor authentications. 

## User Education on Privacy Protection

All the defenses above would be broken if Billy was not careful. Billy should keep the phone nearby all the time. They should never give Alex the phone. Billy might be used to seek help from Alex but this should be stopped. They should never log in to these accounts in the shared PC too.

## Periodic Follow-up Examinations

To ensure the effectiveness of the measures, periodic follow-up examinations would be necessary. There might be loopholes in the plan, flaws in the execution, or slip-ups in securing the phone. Luckily, major service providers showed users all record of login activities nowadays. It would be pretty easy to check if Alex broke into Billy's accounts.

# Planned Procedure

I will not show any screenshots here. UI changes frequently. It is very easy to Google the screenshots if you get lost. You will need to modify it to fit your needs as well.

## Disabling Mobile Network

1. Swipe from the bottom of the screen up to show the control center. 
1. Tap the (green) tower icon.

## iTunes Backup

1. Connect the phone to the PC.
1. Click the small phone icon in iTunes.
1. Confirm if there is no sensitive data on the phone.
1. If there is sensitive data, enable password-protected backup in iTunes. Remember to disable it later.
1. Click the backup button to backup the whole phone.

## Downloading Original Photos and Videos

1. Check data usage of iCloud photos by going to Settings → Apple ID → iCloud → Manage Storage.
1. Check local free disk space and data usage of the Photos app by going to Settings → iPhone Storage.
1. Proceed if the free disk space plus the data usage of the Photos app is more than the data usage of iCloud photos.
1. Download the photos by going to Settings → Photos → select Download and Keep Originals.
1. Open Photos → the Photos tab.
1. Wait for the download to complete as shown at the bottom.

## iTunes Backup Again

1. Connect the phone to the PC.
1. Click the small phone icon in iTunes.
1. Click the "Backup" button to backup the whole phone.

## Separate Photos and Videos Backup

Live photos and burst shots are not copied by this method. 

1. Unplug then plug the phone into a PC.
1. Select "Trust" in the "Trust This Computer" prompt on the phone.
1. Open the phone like a USB stick in the file explorer on the PC.
1. Copy the enclosing folder to the PC.
1. Check the size of the copied folder.
1. At least open some photos to check the integrity.

## Taking Back Accounts

The basic ideas are to sign out all other devices, reset all recovery methods and passwords, and enable 2-factor authentications. It should be started from the email that was used to registered other services. The following steps work for Google accounts. Those for other major service providers like Microsoft are similar. There should be no new logins on the phone until signing out all iCloud logins on other devices. Otherwise, iCloud backup can be abused to continue to spy on you by restoring the backup on other devices. If you cannot do any of the steps, you will need to create a new one for the corresponding account.

1. Login in a browser on a PC.
1. Go to Account Settings → Security → Your Devices → Manage devices.
1. Sign out all other devices.
1. Under "Ways that we can verify that it's you", remove recovery emails and phones which are under other people's control. These steps apply to all recovery accounts and all recovery accounts of them.
1. Change all other recovery methods, e.g. security questions, if there are any.
1. Change the password.
1. Enable 2-Step Verification with SMS.

### Sign out of Other Whatsapp Logins

1. Open Whatsapp.
1. Open Settings.
1. Tap WhatsApp Web/Desktop.
1. Remove all devices listed there. Being asked to scan a QR code means that there are currently no other logins.

## Spyware Removal

1. Open Settings.
1. Scroll down to tap Privacy.
1. Tap Location Services.
1. Check for unknown Apps.
1. Tap back.
1. Check for unknown Apps under Camera and Microphone too.
1. Go back to the home screen.
1. Check for unknown Apps one by one.
1. Delete any unknown and preferably unused Apps.
1. If you remove any apps, do an iTunes backup again.

## Jailbreak Removal

I am not a jailbreak expert. I am not sure if it is possible to hide jailbreak status. I could not find any resources online. My guess is that hiding jailbreak status should be possible when ones have root access. There are apps to hide some other apps on the home screen (SpringBoard). If you want to be sure, it is better to do a DFU restore anyway.

1. Check if there is an app called Cydia. Continue if yes.
1. Sign out iCloud.
1. Backup using the PC again.
1. Do a DFU restore.
1. Restore the phone from the PC.
1. Do an iTunes backup again.

## iCloud Account Migration

Suppose that you cannot take back the iCloud account, you will need to migrate to a new iCloud account.

### Disabling Mobile Data to Prevent Accidental Usage

1. Swipe from the bottom of the screen up to show the control center. 
1. Tap the (green) tower icon.

### Sign out of the Old Apple ID

If your data is very important, you should consider testing your iTunes backups by restorting them to another phone first. A backup that cannot be restored is not a backup.

1. Open Settings.
1. Tap your Apple ID.
1. Scroll down to tap Sign Out.
1. Enable keeping data for all entries in the prompt.

### Sign in of the New Apple ID

1. Open Settings.
1. Tap Apple ID.
1. Fill in the email address and password.
1. Select merge when you are asked to merge the data.
1. Enable appropriate apps under Settings → Apple ID → iCloud → APPS USING ICLOUD.
1. Wait for the synchronization to complete.

## Clean up

1. Re-enable mobile data.
1. Disable password-protected iTunes backup if it is enabled in the previous steps.
1. Delete the iTunes backups.
1. Delete the manual photo backup.

## Strengthening Security

### Disabling SMS on the Lock Screen

Option 1: disabling previews

1. Open Settings.
1. Tap Notifications.
1. Tap Messages.
1. Select Never for Show Previews.

Option 2: disabling previews on the lock screen only

1. Open Settings.
1. Tap Notifications.
1. Tap Messages.
1. Deselect Lock Screen.

## Disabling Fingerprint Unlock

1. Open Settings.
1. Scroll down to and tap Touch ID & Passcode.
1. Disable iPhone Unlock under USE TOUCH ID FOR.

## Enabling Find My Phone (iCloud Lock)

1. Open Settings.
1. Tap your Apple ID.
1. Tap Find My.
1. Tap Find My Phone.
1. Switch on Find My Phone.

# Routine Maintenance

The following items should be checked or performed periodically.

## Disabling SMS on The Lock Screen

Option 1: disabling previews

1. Open Settings.
1. Tap Notifications.
1. Tap Messages.
1. Select Never for Show Previews.

Option 2: disabling previews on the lock screen only

1. Open Settings.
1. Tap Notifications.
1. Tap Messages.
1. Deselect Lock Screen.

## Disabling Fingerprint Lock

1. Open Settings.
1. Scroll down to and tap Touch ID & Passcode.
1. Disable iPhone Unlock under USE TOUCH ID FOR.

## Enabling Find My Phone (iCloud Lock)

1. Open Settings.
1. Tap your Apple ID.
1. Tap Find My.
1. Tap Find My Phone.
1. Switch on Find My Phone.

## Checking Whatsapp Login Activity

1. Open Whatsapp.
1. Open Settings.
1. Tap WhatsApp Web/Desktop.
1. Being asked to scan a QR code means that there are currently no other logins.

## Google Account Security

Check for no suspicious logins, extra 2-step verification methods, and password recovery methods.

1. Log in to [https://www.google.com](https://www.google.com) in a browser with the password to verify if it was unchanged.
1. Click the account icon.
1. Click Manage your Google A/C.
1. Click Security.
1. Under Signing in to Google, 2-Step Verification, there are
   1. no Authenticator app
   1. no Backup codes
   1. no Google prompts
   1. only the correct phone number in Voice or text message 
   1. no Security Key
   1. no Devices you trust
6. Under Signing in to Google, there are no entries in App passwords.
7. Under Ways we can verify it's you, only the correct phone number in recovery phones and no recovery emails.
8. Under Recent security activity, there are no unknown logins.
9. Under Your devices, there are no other devices.
10. Under Signing in to other sites, there are no entries in Third-party apps with account access and each category.

## Apple ID

1. Log in to [https://appleid.apple.com](https://appleid.apple.com) in a browser with the password to verify if it was unchanged.
2. Click the edit button in the security section.
3. There is only the correct phone number under TRUSTED PHONE NUMBERS.
4. There is no view history under APP-SPECIFIC PASSWORDS.
5. TWO-FACTOR AUTHENTICATION is on.
6. There is only the phone in Devices.

# Execution

The process took only 3 - 4 hours, greatly thanks to friend D being an above-average computer user and an extra phone for showing me their screens. We spent quite a substantial amount of time trying to take the accounts back. We could not take Billy's Microsoft email account back because of not knowing the password and answers to the security questions. We applied for a review of our declaration of our ownership of the account. We could not take iCloud account back too so we did an iCloud migration. There were only small deviations from the plan which they were easy to deal with. There was time for me to educate Billy on how to protect their digital privacy.

# Result

A few days later, Alex sneakily attempted to take Billy's phone and acted suspiciously. This was a sign of temporary success. However, I suspected that Alex knew the password of the phone. Billy ensured that Alex did not know the password of the phone. It was a stressful enough situation so I did not push Billy to use a new password.

We did not receive any responses from Microsoft so the email account was lost forever. Billy would notify their friends of the new email address in person. To ensure the security would hold, friend D would help Billy to perform the routine maintenance. That was the best we could do for the moment.

# Conclusion

The procedure was lengthy and might seem complicated to most people. It was harder to defend than attack. One did not know how their adversaries would attack so the defense had to thoroughly cover all angles. The procedure was slightly different from the best practice for digital security. It was required to suit the rather unusual situation. It was unfortunate that we could not take back all accounts.