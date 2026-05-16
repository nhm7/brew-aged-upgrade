# typed: false
# frozen_string_literal: true

class BrewAgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  depends_on "python@3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
